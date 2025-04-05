from app.views import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import openpyxl
from django.http import HttpResponse
from app.models import Partner

@method_decorator(csrf_exempt, name="dispatch")
class PartnerCreateView(CreateView):
    model = Partner
    form_class = PartnerForm
    template_name = 'create.html'
    success_url = reverse_lazy('successfully_created')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание партнера'
        context['form'].fields['fillial'].initial = self.request.GET.get('fillial')
        context['form'].fields['fillial'].label = ""
        return context


def export_partners_to_excel(request):
    # Create a new workbook and select the active worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = "Partners"

    # Define the headers
    headers = ["Имя"]

    # Write the headers to the first row
    worksheet["A1"] = headers[0]

    # Write data rows
    for row_num, partner in enumerate(Partner.objects.all(), 2):
        worksheet[f"A{row_num}"] = partner.name

    # Set the width of the column for better readability
    worksheet.column_dimensions['A'].width = 30  # Adjust the width as needed

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="partners.xlsx"'
    workbook.save(response)
    return response
