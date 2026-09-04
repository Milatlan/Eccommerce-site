from pathlib import Path

api = Path('backend/tracker/mobile_api.py')
s = api.read_text(encoding='utf-8')
if 'def client_create(request):' not in s:
    s = s.replace('from django.http import HttpResponse, JsonResponse\n', 'from django.http import HttpResponse, JsonResponse\nfrom django.db.models import Max\n')
    s = s.replace('from django.utils.dateparse import parse_date\n', 'from django.utils.dateparse import parse_date\nfrom django.utils.text import slugify\n')
    marker = '@require_GET\n@mobile_api_required\ndef day_state(request):'
    block = '''@csrf_exempt\n@require_POST\n@mobile_api_required\ndef client_create(request):\n    body = _json_body(request)\n    if body is None:\n        return JsonResponse({'ok': False, 'error': 'Invalid request data.'}, status=400)\n    name = ' '.join((body.get('name') or '').strip().split())[:120]\n    if not name:\n        return JsonResponse({'ok': False, 'error': 'Client name is required.'}, status=400)\n    if Client.objects.filter(name__iexact=name).exists():\n        return JsonResponse({'ok': False, 'error': 'That client already exists.'}, status=409)\n    base_slug = slugify(name)[:120] or 'client'\n    slug = base_slug\n    suffix = 2\n    while Client.objects.filter(slug=slug).exists():\n        suffix_text = f'-{suffix}'\n        slug = f'{base_slug[:140-len(suffix_text)]}{suffix_text}'\n        suffix += 1\n    next_order = (Client.objects.aggregate(max_order=Max('sort_order'))['max_order'] or 0) + 10\n    client = Client.objects.create(name=name, slug=slug, sort_order=next_order, active=True)\n    return JsonResponse({'ok': True, 'client': {'id': client.id, 'name': client.name, 'slug': client.slug, 'sort_order': client.sort_order}}, status=201)\n\n\n'''
    if marker not in s:
        raise SystemExit('day_state marker not found')
    s = s.replace(marker, block + marker)
    api.write_text(s, encoding='utf-8')

urls = Path('backend/tracker/urls.py')
u = urls.read_text(encoding='utf-8')
line = "    path('api/mobile/clients/', mobile_api.client_create, name='mobile_client_create'),\n"
if line not in u:
    anchor = "    path('api/mobile/employees/', mobile_api.employee_create, name='mobile_employee_create'),\n"
    if anchor not in u:
        raise SystemExit('employee route marker not found')
    u = u.replace(anchor, anchor + line)
    urls.write_text(u, encoding='utf-8')
print('S2S mobile client-create API patched.')
