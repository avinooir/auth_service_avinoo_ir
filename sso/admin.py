"""
SSO Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import SSOClient, SSOSession, SSOAuditLog


@admin.register(SSOClient)
class SSOClientAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'domain', 'client_id', 'is_active', 
        'allow_any_path', 'redirect_uri_short', 'created_at'
    ]
    list_filter = ['is_active', 'allow_any_path', 'created_at', 'updated_at']
    search_fields = ['name', 'domain', 'client_id', 'client_secret']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_editable = ['is_active', 'allow_any_path']
    
    fieldsets = (
        ('اطلاعات کلاینت', {
            'fields': ('name', 'domain', 'client_id', 'client_secret')
        }),
        ('تنظیمات بازگشت', {
            'fields': ('redirect_uri', 'allowed_redirect_uris', 'allow_any_path'),
            'description': 'تنظیمات مربوط به آدرس‌های بازگشت مجاز'
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
        ('اطلاعات سیستم', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def redirect_uri_short(self, obj):
        """نمایش کوتاه redirect_uri"""
        if obj.redirect_uri:
            return obj.redirect_uri[:50] + '...' if len(obj.redirect_uri) > 50 else obj.redirect_uri
        return '-'
    redirect_uri_short.short_description = 'آدرس بازگشت'
    
    def get_queryset(self, request):
        return super().get_queryset(request)
    
    actions = ['activate_clients', 'deactivate_clients', 'toggle_allow_any_path']
    
    def activate_clients(self, request, queryset):
        """فعال کردن کلاینت‌های انتخاب شده"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} کلاینت فعال شد.')
    activate_clients.short_description = 'فعال کردن کلاینت‌های انتخاب شده'
    
    def deactivate_clients(self, request, queryset):
        """غیرفعال کردن کلاینت‌های انتخاب شده"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} کلاینت غیرفعال شد.')
    deactivate_clients.short_description = 'غیرفعال کردن کلاینت‌های انتخاب شده'
    
    def toggle_allow_any_path(self, request, queryset):
        """تغییر وضعیت allow_any_path"""
        for client in queryset:
            client.allow_any_path = not client.allow_any_path
            client.save()
        self.message_user(request, f'وضعیت allow_any_path برای {queryset.count()} کلاینت تغییر کرد.')
    toggle_allow_any_path.short_description = 'تغییر وضعیت Allow Any Path'
    
    def get_urls(self):
        """اضافه کردن URL های سفارشی"""
        urls = super().get_urls()
        custom_urls = [
            path('client-details/<uuid:client_id>/', 
                 self.admin_site.admin_view(self.client_details_view),
                 name='sso_ssoclient_details'),
        ]
        return custom_urls + urls
    
    def client_details_view(self, request, client_id):
        """نمایش جزئیات کلاینت"""
        try:
            client = SSOClient.objects.get(id=client_id)
            
            # آمار جلسات این کلاینت
            sessions = SSOSession.objects.filter(client=client)
            active_sessions = sessions.filter(expires_at__gt=timezone.now())
            expired_sessions = sessions.filter(expires_at__lt=timezone.now())
            
            # آمار لاگ‌های این کلاینت
            logs = SSOAuditLog.objects.filter(client=client)
            login_logs = logs.filter(action='login')
            logout_logs = logs.filter(action='logout')
            
            context = {
                'title': f'جزئیات کلاینت: {client.name}',
                'client': client,
                'sessions': {
                    'total': sessions.count(),
                    'active': active_sessions.count(),
                    'expired': expired_sessions.count(),
                },
                'logs': {
                    'total': logs.count(),
                    'login': login_logs.count(),
                    'logout': logout_logs.count(),
                },
                'recent_sessions': sessions.order_by('-created_at')[:10],
                'recent_logs': logs.order_by('-created_at')[:10],
            }
            
            return render(request, 'admin/client_details.html', context)
            
        except SSOClient.DoesNotExist:
            messages.error(request, 'کلاینت مورد نظر یافت نشد.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/admin/'))


@admin.register(SSOSession)
class SSOSessionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'client', 'state_short', 'is_used', 
        'expires_status', 'created_at', 'expires_at'
    ]
    list_filter = ['is_used', 'created_at', 'expires_at', 'client__name']
    search_fields = ['user__username', 'user__email', 'client__name', 'state', 'redirect_uri']
    readonly_fields = ['id', 'created_at', 'expires_at']
    list_editable = ['is_used']
    
    fieldsets = (
        ('اطلاعات جلسه', {
            'fields': ('user', 'client', 'state', 'redirect_uri')
        }),
        ('وضعیت جلسه', {
            'fields': ('is_used', 'expires_at')
        }),
        ('اطلاعات سیستم', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def state_short(self, obj):
        """نمایش کوتاه state"""
        if obj.state:
            return obj.state[:20] + '...' if len(obj.state) > 20 else obj.state
        return '-'
    state_short.short_description = 'وضعیت'
    
    def expires_status(self, obj):
        """نمایش وضعیت انقضا"""
        now = timezone.now()
        if obj.expires_at > now:
            return format_html('<span style="color: green;">✅ فعال</span>')
        else:
            return format_html('<span style="color: red;">❌ منقضی</span>')
    expires_status.short_description = 'وضعیت انقضا'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'client')
    
    actions = ['mark_as_used', 'mark_as_unused', 'delete_expired_sessions']
    
    def mark_as_used(self, request, queryset):
        """علامت‌گذاری جلسات به عنوان استفاده شده"""
        updated = queryset.update(is_used=True)
        self.message_user(request, f'{updated} جلسه به عنوان استفاده شده علامت‌گذاری شد.')
    mark_as_used.short_description = 'علامت‌گذاری به عنوان استفاده شده'
    
    def mark_as_unused(self, request, queryset):
        """علامت‌گذاری جلسات به عنوان استفاده نشده"""
        updated = queryset.update(is_used=False)
        self.message_user(request, f'{updated} جلسه به عنوان استفاده نشده علامت‌گذاری شد.')
    mark_as_unused.short_description = 'علامت‌گذاری به عنوان استفاده نشده'
    
    def delete_expired_sessions(self, request, queryset):
        """حذف جلسات منقضی شده"""
        now = timezone.now()
        expired_sessions = queryset.filter(expires_at__lt=now)
        count = expired_sessions.count()
        expired_sessions.delete()
        self.message_user(request, f'{count} جلسه منقضی شده حذف شد.')
    delete_expired_sessions.short_description = 'حذف جلسات منقضی شده'


@admin.register(SSOAuditLog)
class SSOAuditLogAdmin(admin.ModelAdmin):
    list_display = [
        'action', 'action_display', 'user', 'client', 
        'ip_address', 'user_agent_short', 'created_at'
    ]
    list_filter = ['action', 'created_at', 'client__name']
    search_fields = [
        'user__username', 'user__email', 'client__name', 
        'ip_address', 'user_agent', 'details'
    ]
    readonly_fields = ['id', 'created_at', 'all_fields_readonly']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات فعالیت', {
            'fields': ('action', 'user', 'client')
        }),
        ('اطلاعات شبکه', {
            'fields': ('ip_address', 'user_agent')
        }),
        ('جزئیات', {
            'fields': ('details',),
            'classes': ('collapse',)
        }),
        ('اطلاعات سیستم', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def action_display(self, obj):
        """نمایش فارسی action"""
        action_map = {
            'login': 'ورود',
            'logout': 'خروج',
            'token_issued': 'صدور توکن',
            'token_validated': 'اعتبارسنجی توکن',
            'redirect': 'انتقال',
            'error': 'خطا',
        }
        return action_map.get(obj.action, obj.action)
    action_display.short_description = 'نوع فعالیت'
    
    def user_agent_short(self, obj):
        """نمایش کوتاه user agent"""
        if obj.user_agent:
            return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
        return '-'
    user_agent_short.short_description = 'User Agent'
    
    def all_fields_readonly(self, obj):
        """نمایش تمام فیلدها به صورت readonly"""
        if obj:
            return format_html(
                '<strong>این رکورد فقط خواندنی است و نمی‌توان آن را ویرایش کرد.</strong>'
            )
        return ''
    all_fields_readonly.short_description = 'نکته'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'client')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    actions = ['delete_old_logs', 'export_logs']
    
    def delete_old_logs(self, request, queryset):
        """حذف لاگ‌های قدیمی (بیش از 30 روز)"""
        from datetime import timedelta
        cutoff_date = timezone.now() - timedelta(days=30)
        old_logs = queryset.filter(created_at__lt=cutoff_date)
        count = old_logs.count()
        old_logs.delete()
        self.message_user(request, f'{count} لاگ قدیمی (بیش از 30 روز) حذف شد.')
    delete_old_logs.short_description = 'حذف لاگ‌های قدیمی (بیش از 30 روز)'
    
    def export_logs(self, request, queryset):
        """صادرات لاگ‌های انتخاب شده"""
        import csv
        from django.http import HttpResponse
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="sso_audit_logs.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID', 'Action', 'User', 'Client', 'IP Address', 
            'User Agent', 'Details', 'Created At'
        ])
        
        for log in queryset:
            writer.writerow([
                log.id,
                log.action,
                log.user.username if log.user else 'Anonymous',
                log.client.name if log.client else 'Unknown',
                log.ip_address,
                log.user_agent[:100] if log.user_agent else '',
                str(log.details)[:100] if log.details else '',
                log.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        self.message_user(request, f'{queryset.count()} لاگ صادر شد.')
        return response
    export_logs.short_description = 'صادرات لاگ‌های انتخاب شده'


# Admin Actions برای مدیریت کلی SSO
@admin.action(description='نمایش آمار SSO')
def show_sso_stats(modeladmin, request, queryset):
    """نمایش آمار کلی SSO"""
    from django.db.models import Count
    from datetime import timedelta
    
    now = timezone.now()
    last_24h = now - timedelta(hours=24)
    last_7d = now - timedelta(days=7)
    last_30d = now - timedelta(days=30)
    
    # آمار کلاینت‌ها
    total_clients = SSOClient.objects.count()
    active_clients = SSOClient.objects.filter(is_active=True).count()
    
    # آمار جلسات
    total_sessions = SSOSession.objects.count()
    active_sessions = SSOSession.objects.filter(expires_at__gt=now).count()
    expired_sessions = SSOSession.objects.filter(expires_at__lt=now).count()
    
    # آمار لاگ‌ها
    total_logs = SSOAuditLog.objects.count()
    logs_24h = SSOAuditLog.objects.filter(created_at__gte=last_24h).count()
    logs_7d = SSOAuditLog.objects.filter(created_at__gte=last_7d).count()
    logs_30d = SSOAuditLog.objects.filter(created_at__gte=last_30d).count()
    
    # آمار فعالیت‌ها
    login_logs = SSOAuditLog.objects.filter(action='login').count()
    logout_logs = SSOAuditLog.objects.filter(action='logout').count()
    token_validations = SSOAuditLog.objects.filter(action='token_validated').count()
    
    # آمار کاربران فعال
    active_users_24h = SSOAuditLog.objects.filter(
        created_at__gte=last_24h,
        action='login'
    ).values('user').distinct().count()
    
    context = {
        'title': 'آمار SSO',
        'total_clients': total_clients,
        'active_clients': active_clients,
        'total_sessions': total_sessions,
        'active_sessions': active_sessions,
        'expired_sessions': expired_sessions,
        'total_logs': total_logs,
        'logs_24h': logs_24h,
        'logs_7d': logs_7d,
        'logs_30d': logs_30d,
        'login_logs': login_logs,
        'logout_logs': logout_logs,
        'token_validations': token_validations,
        'active_users_24h': active_users_24h,
    }
    
    return render(request, 'admin/sso_stats.html', context)


# اضافه کردن action به تمام مدل‌های SSO
SSOClientAdmin.actions = SSOClientAdmin.actions + [show_sso_stats]
SSOSessionAdmin.actions = SSOSessionAdmin.actions + [show_sso_stats]
SSOAuditLogAdmin.actions = SSOAuditLogAdmin.actions + [show_sso_stats]


# Admin Action برای پاک کردن جلسات منقضی شده
@admin.action(description='پاک کردن جلسات منقضی شده')
def cleanup_expired_sessions(modeladmin, request, queryset):
    """پاک کردن جلسات منقضی شده"""
    now = timezone.now()
    expired_sessions = SSOSession.objects.filter(expires_at__lt=now)
    count = expired_sessions.count()
    expired_sessions.delete()
    
    messages.success(request, f'{count} جلسه منقضی شده پاک شد.')
    return HttpResponseRedirect(request.get_full_path())


# اضافه کردن action پاکسازی به SSOSessionAdmin
SSOSessionAdmin.actions = SSOSessionAdmin.actions + [cleanup_expired_sessions]
