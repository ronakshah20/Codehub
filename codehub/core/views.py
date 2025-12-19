from django.shortcuts import render, redirect
# Create your views here.

from django.contrib.auth.decorators import login_required # Import the decorator
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.core.files.uploadedfile import UploadedFile
from .models import Repository, RepoFile
import json
import io
from io import BytesIO
import sys
import contextlib
import base64
import builtins
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import zipfile

@login_required(login_url='/accounts/login/')
def dashboard_view(request):
    """
    Displays repositories for the logged-in user:
    - user_repos: all repos owned by the user (public + private)
    - other_public_repos: public repos from other users
    """
    # Owned by user (any visibility)
    user_repos = Repository.objects.filter(owner=request.user).order_by('-updated_at')

    # Public repos from others
    other_public_repos = Repository.objects.filter(
        visibility='public'
    ).exclude(owner=request.user).order_by('-updated_at')

    return render(request, "dashboard.html", {
        "user_repos": user_repos,
        "other_public_repos": other_public_repos,
    })

@login_required(login_url='/accounts/login/')
def create_repo_view(request):
    """
    Handles new repository creation and assigns the current user as the owner.
    """
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        visibility = request.POST.get("visibility")

        Repository.objects.create(
            owner=request.user,
            name=name,
            description=description,
            visibility=visibility,
        )
        return redirect("dashboard")
        
    return render(request, "createrepo.html")

@login_required(login_url='/accounts/login/')
def python_env_view(request):
    """
    Renders the Python code execution environment page.
    """
    return render(request, "python_environment.html")

class CapturingInput:
    """
    A context manager to capture 'input()' calls.
    """
    def __init__(self, inputs_list, current_index):
        self.inputs_list = inputs_list
        self.current_index = current_index
        self._original_input = builtins.input
        self.prompt = ""

    def __enter__(self):
        builtins.input = self.mock_input
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        builtins.input = self._original_input

    def mock_input(self, prompt=""):
        self.prompt = prompt
        if self.current_index < len(self.inputs_list):
            value = self.inputs_list[self.current_index]
            self.current_index += 1
            return value
        else:
            # Not enough inputs provided, raise an exception to signal for more.
            raise EOFError("Input required")


# --- VIEW 2: THE CODE EXECUTION API ---

def run_code_view(request):
    """
    Executes Python code from the API.
    Handles standard output, matplotlib plots, and 'input()' prompts.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        inputs = data.get('inputs', [])
        input_index = data.get('input_index', 0)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    if not code.strip():
        return JsonResponse({
            'status': 'error',
            'output': 'Error: No code provided'
        })
    # Prepare to capture stdout
    stdout_capture = io.StringIO()
    
    # Prepare to capture matplotlib plots
    plt.close('all') # Clear any previous plots
    img_buffer = io.BytesIO()

    try:
        # Execute the code
        with contextlib.redirect_stdout(stdout_capture):
            with CapturingInput(inputs, input_index) as input_handler:
                exec(code, {"__builtins__": __builtins__})
        
        # If code finished without needing more input
        output = stdout_capture.getvalue()
        
        # Check if a plot was created and save it
        img_base64 = None
        if plt.get_fignums(): # Check if any figures exist
            plt.savefig(img_buffer, format='png', bbox_inches='tight')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

        return JsonResponse({
            'status': 'success',
            'output': output,
            'image': img_base64,
            'html': None # You can add logic for Folium/Plotly here if needed
        })

    except EOFError:
        # 'input()' was called but we ran out of inputs
        return JsonResponse({
            'status': 'input_required',
            'prompt': input_handler.prompt or "Enter input:",
            'next_input_index': input_handler.current_index,
            'output': stdout_capture.getvalue() # Send partial output
        })
    except Exception as e:
        # Code execution failed
        return JsonResponse({
            'status': 'error',
            'output': stdout_capture.getvalue() + f"\n--- EXECUTION ERROR ---\n{type(e).__name__}: {e}"
        })
    finally:
        plt.close('all') # Always clean up plot figures

@login_required(login_url='/accounts/login/')
def repository_detail_view(request, username, repo_name):
    """
    Displays the file list and details for a single repository.
    """
    # 1. Get the repository owner and the repository
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    # 2. Check for private repository access
    if repo.visibility == 'private' and request.user != repo.owner:
        # (Later, you can add logic here for collaborators)
        return redirect('dashboard') # Or show a 404/Permission Denied

    # 3. Get all files for this repository from the new model
    files = repo.files.all().order_by('file_path')

    context = {
        'repo': repo,
        'files': files,
    }
    
    return render(request, "repository_detail.html", context)

@login_required(login_url='/accounts/login/')
def repository_settings_view(request, username, repo_name):
    """
    Simple repository settings page (placeholder).
    Only the owner can access.
    """
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    if request.user != repo.owner:
        messages.error(request, "You don't have permission to access repository settings.")
        return redirect('repository_detail', username=username, repo_name=repo_name)

    # For now, just show basic info; can be extended later
    return render(request, "repository_settings.html", {"repo": repo})


@login_required(login_url='/accounts/login/')
def edit_repository_view(request, username, repo_name):
    """
    Edit repository name, description, and visibility.
    Only the owner can edit.
    """
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    if request.user != repo.owner:
        messages.error(request, "You don't have permission to edit this repository.")
        return redirect('repository_detail', username=username, repo_name=repo_name)

    if request.method == "POST":
        new_name = request.POST.get("name", "").strip()
        new_description = request.POST.get("description", "").strip()
        new_visibility = request.POST.get("visibility", "public")

        if not new_name:
            messages.error(request, "Repository name is required.")
            return render(request, "edit_repository.html", {"repo": repo})

        repo.name = new_name
        repo.description = new_description
        repo.visibility = new_visibility
        repo.save()

        messages.success(request, "Repository updated successfully.")
        return redirect('repository_detail', username=repo.owner.username, repo_name=repo.name)

    return render(request, "edit_repository.html", {"repo": repo})


@login_required(login_url='/accounts/login/')
def delete_repository_view(request, username, repo_name):
    """
    Delete a repository. Only via POST and only by owner.
    """
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    if request.user != repo.owner:
        messages.error(request, "You don't have permission to delete this repository.")
        return redirect('repository_detail', username=username, repo_name=repo_name)

    if request.method == "POST":
        repo_name_saved = repo.name
        repo.delete()
        messages.success(request, f"Repository '{repo_name_saved}' deleted successfully.")
        return redirect("dashboard")

    # If GET, show a simple confirm page or redirect back
    messages.error(request, "Invalid request method for deleting repository.")
    return redirect('repository_detail', username=username, repo_name=repo_name)


@login_required(login_url='/accounts/login/')
def download_repository_view(request, username, repo_name):
    """
    Download entire repository as a ZIP file.
    Only the owner can download for now.
    """
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    # Permission check: owner only (you can relax this later for public repos)
    if request.user != repo.owner:
        messages.error(request, "You don't have permission to download this repository.")
        return redirect('repository_detail', username=username, repo_name=repo_name)

    # Create an in-memory ZIP file
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for f in repo.files.all():
            # Skip folder placeholders if you ever add them
            if hasattr(f, "is_folder") and f.is_folder:
                continue
            zip_file.writestr(f.file_path, f.content or "")

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment; filename="{repo.name}.zip"'
    return response


@login_required(login_url='/accounts/login/')
def create_file_view(request, username, repo_name):
    """
    Handles the creation of a new file within a repository.
    GET: Displays the file editor.
    POST: Saves the new file.
    """
    # 1. Get the repository
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    # 2. Security Check: Only the owner can create files
    if request.user != repo.owner:
        return redirect('repository_detail', username=username, repo_name=repo_name)

    # 3. Handle the form submission
    if request.method == "POST":
        file_path = request.POST.get("file_path")
        content = request.POST.get("content")

        if not file_path:
            # Handle error: file path is required
            context = {'repo': repo, 'error': 'File name is required.'}
            return render(request, "create_file.html", context)
        
        # Create the new file in the database
        RepoFile.objects.create(
            repository=repo,
            file_path=file_path,
            content=content
        )
        
        # Redirect back to the repository's main page
        return redirect('repository_detail', username=username, repo_name=repo_name)

    # 4. Handle the initial page load (GET request)
    context = {
        'repo': repo,
    }
    
    return render(request, "create_file.html", context)

@login_required(login_url='/accounts/login/')
def edit_file_view(request, username, repo_name, file_id):
    """
    Handles editing an existing file in a repository.
    GET: Displays the editor with the file's current content.
    POST: Saves the updated content.
    """
    # 1. Get the repository and the specific file
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    file_to_edit = get_object_or_404(RepoFile, repository=repo, id=file_id)

    # 2. Security Check: Only the owner can edit files
    if request.user != repo.owner:
        return redirect('repository_detail', username=username, repo_name=repo_name)

    # 3. Handle the form submission (saving changes)
    if request.method == "POST":
        # Get the new content from the form
        content = request.POST.get("content")
        
        # Update the file's content and save it
        file_to_edit.content = content
        file_to_edit.save()
        
        # Redirect back to the repository's main page
        return redirect('repository_detail', username=username, repo_name=repo_name)

    # 4. Handle the initial page load (GET request)
    context = {
        'repo': repo,
        'file_to_edit': file_to_edit,
    }
    
    return render(request, "edit_file.html", context)

@login_required(login_url='/accounts/login/')
def delete_file_view(request, username, repo_name, file_id):
    """
    Handles deleting an existing file from a repository.
    This view only accepts POST requests for security.
    """
    # 1. Get the repository and the specific file
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    file_to_delete = get_object_or_404(RepoFile, repository=repo, id=file_id)

    # 2. Security Check: Only the owner can delete files
    if request.user != repo.owner:
        return redirect('repository_detail', username=username, repo_name=repo_name)

    # 3. We only allow deletion via POST (from a form) to prevent
    #    accidental deletion from a simple link.
    if request.method == "POST":
        file_to_delete.delete()
        
    # 4. Redirect back to the repository's main page
    #    (This happens after a POST or if it was a GET request)
    return redirect('repository_detail', username=username, repo_name=repo_name)

@login_required(login_url='/accounts/login/')
def upload_file_view(request, username, repo_name):
    """
    Upload a single text file into the repository.
    Only owner can upload.
    """
    owner = get_object_or_404(User, username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)

    if request.user != repo.owner:
        messages.error(request, "You don't have permission to upload to this repository.")
        return redirect('repository_detail', username=username, repo_name=repo_name)

    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            messages.error(request, "No file selected.")
            return redirect('repository_detail', username=username, repo_name=repo_name)

        # For now, put file at root with its name; no folders
        file_path = uploaded_file.name

        # Read content as text (assuming UTF‑8 source code / text files)
        content_bytes = uploaded_file.read()
        try:
            content = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            content = ""  # or you could store binary differently

        # Create RepoFile (or overwrite if same path exists)
        existing = RepoFile.objects.filter(repository=repo, file_path=file_path).first()
        if existing:
            existing.content = content
            existing.save()
        else:
            RepoFile.objects.create(
                repository=repo,
                file_path=file_path,
                content=content,
            )

        messages.success(request, f"File '{file_path}' uploaded successfully.")
        return redirect('repository_detail', username=username, repo_name=repo_name)

    # For GET, a simple upload page
    return render(request, "upload_file.html", {"repo": repo})
