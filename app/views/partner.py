from app.views import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name="dispatch")
class PartnerCreateView(CreateView):
    model = Partner
    form_class = PartnerForm
    template_name = 'create.html'
    success_url = reverse_lazy('successfully_created')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание партнера'
        return context