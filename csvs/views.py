from django.shortcuts import render
from .forms import CsvModeForm
from django.http import HttpResponse
from .models import CSV
from django.contrib.auth.models import User
import csv
from sales.models import Sale
# Create your views here.
def upload_file_view(request):
    form = CsvModeForm(request.POST or None , request.FILES or None)
    if(form.is_valid()):
        form.save()
        form = CsvModeForm()
        obj = CSV.objects.get(activated= False)
        #đọc dữ liệu từ 1 tệp
        
        with open(obj.file_name.path, 'r', encoding = 'unicode_escape') as f:
            reader = csv.reader(f)
            #bỏ qua hàng đầu tiên(hàng tiêu đề)
            #emumerate: trình đọc số
            for i, row in enumerate(reader):
                if i ==0:
                    pass
                else:
                    row = "".join(row)
                    row = row.replace(";", "")
                    row = row.split()
                    product = row[1].upper()
                    user = User.objects.get(username=row[3])
                    Sale.objects.create(
                        product = product,
                        quantity = int(row[2]),
                        salesman = user ,
                    )
                    # print(row)
                    # print(type(row)) #str
            obj.activated = True
            obj.save()
    return render(request, 'csvs/upload.html', {'form': form})
