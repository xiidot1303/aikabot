from app.views import *
import os
from core.settings import BASE_DIR

def get_file(request, path):
    file = open(os.path.join(BASE_DIR, f'files/{path}'), 'rb')
    return FileResponse(file)

async def successfully_created(request):
    return render(request, 'successfully_created.html')