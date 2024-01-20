from django.shortcuts import redirect, render

def sku_entry(request):
    lp = request.session.get('lp')
    if lp is None:
        return redirect('MDlogger:associate_home')
    if request.method == "POST":
        sku = request.POST.get('sku')
        request.session['sku'] = sku
        return redirect('MDlogger:add_repair')
    return render(request, 'MDlogger/sku_entry.html', {'lp': lp})