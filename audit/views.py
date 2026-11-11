from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from audit.audit_service import run_full_audit


@csrf_exempt
def start_audit(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        if not url:
            return JsonResponse({'error': 'URL required'}, status=400)
        
        result = run_full_audit(url)
        return JsonResponse(result, safe=False)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def index(request):
    return render(request, 'audit/index.html')
