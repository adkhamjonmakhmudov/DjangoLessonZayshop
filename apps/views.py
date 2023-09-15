from django.contrib.admindocs.views import ModelDetailView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView

from apps.forms import CustomLoginForm, RegisterForm
from apps.models import Category, Product


class AboutPageTemplateView(TemplateView):
    template_name = 'about.html'


class ContactPageTemplateView(TemplateView):
    template_name = 'contact.html'


class HomePageTemplateView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['posts'] = Product.objects.order_by('-created_at')[:6]
        return data


class ShopTemplateView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        pagination = context['page_obj']
        paginator = pagination.paginator
        page = pagination.number
        left = (int(page) - 4)
        if left < 1:
            left = 1
        right = (int(page) + 5)
        if right > paginator.num_pages:
            right = paginator.num_pages + 1
        context['pagination_range'] = range(left, right)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop-single.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['post']
        related_products = Product.objects.filter(category=product.category).exclude(slug=product.slug)
        context['related_products'] = related_products
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.update_views()
        return super().get(request, *args, **kwargs)


class UserProductCreateView(CreateView):
    queryset = Product.objects.all()
    fields = ['name', 'image', 'description', 'price', 'size', 'color', 'category']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        print("Submitted data:", form.cleaned_data)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(" Noto'g'ri ma'lumotlar:", form.errors)
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        print("Jo'natilgan ma'lumotlar:", form.errors)  # noqa
        return super().form_invalid(form)


class CategoryProductsView(DetailView):
    model = Category
    template_name = 'category_products.html'
    context_object_name = 'category_posts'


class CategorySecond(ModelDetailView):
    pass


class CategorySecond3(ModelDetailView):
    pass
