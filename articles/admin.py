from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        check_list = []
        for form in self.forms:
            if len(form.cleaned_data) > 0:
                check_list.append(form.cleaned_data['is_main'])
        if check_list.count(True) > 1:
            raise ValidationError('Основным может быть только один раздел')
        if check_list.count(True) == 0:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 3
    formset = ScopeInlineFormset

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    inlines = [ScopeInline, ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
