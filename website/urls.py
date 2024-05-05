from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('terms/',views.terms,name='terms'),
    path('contact/',views.contact_page,name='contact'),
    path('warrenty/',views.warrenty,name='warrenty'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logoutP,name='logout'),
    path('register/',views.register,name='register'),
    path('newsletter/',views.newsletter_sub,name='newsletter'),
    path('partnership/',views.partnership_form,name='partnership'),
    path('search/',views.SearchDataView,name='search'),
    path('product_page_single/<str:pk>',views.product_page_single,name='product_page_single'),
    path('add_to_watchlist/<str:pk>/', views.add_to_watchlist, name='add_to_watchlist'),
    path('remove_watchlist/<str:pk>/', views.remove_watchlist, name='remove_watchlist'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('filter_search/', views.filter_search, name='filter_search'),
    path('sema2018/', views.sema2018, name='sema2018'),
    path('sema2019/', views.sema2019, name='sema2019'),

    path('initial_data/', views.initial_data, name='initial_data'),
    path('market_filter/', views.market_filter, name='market_filter'),
    path('model_filter/', views.model_filter, name='model_filter'),
    path('body_filter/', views.body_filter, name='body_filter'),
    path('year_filter/', views.year_filter, name='year_filter'),
    path('suspension_filter/', views.suspension_filter, name='suspension_filter'),

    path('add_to_cart/<str:pk>/', views.add_to_cart, name='add_to_cart'),   
    path('cart/', views.cart, name='cart'),
    path('remove_cart/<str:pk>/', views.remove_cart, name='remove_cart'),

    path('add_order/', views.add_order, name='add_order'), 
    path('my_order/', views.my_order, name='my_order'), 
    path('order_approval/<str:pk>/', views.order_approval, name='order_approval'), 
    path('order_disapproval/<str:pk>/', views.order_disapproval, name='order_disapproval'), 
    path('all_orders/', views.all_orders, name='all_orders'),
    path('order_detail/<str:pk>/', views.order_detail, name='order_detail'), 

    path('checkout/', views.checkout, name='checkout'),

    path('all_products/', views.all_products, name='all_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_bulk_product/', views.add_bulk_product, name='add_bulk_product'),
    path('update_product/<str:pk>/', views.update_product, name='update_product'),
    path('copy_product/<str:pk>/', views.copy_product, name='copy_product'),
    path('remove_product/<str:pk>/', views.remove_product, name='remove_product'),

    path('all_discount/', views.all_discount, name='all_discount'),
    path('give_discount/', views.give_discount, name='give_discount'),
    path('update_coupon/<str:pk>/', views.update_coupon, name='update_coupon'),
    path('remove_coupon/<str:pk>/', views.remove_coupon, name='remove_coupon'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('all_contacts/', views.all_contacts, name='all_contacts'),
    path('all_distributors/', views.all_distributors, name='all_distributors'),
    path('all_users/', views.all_users, name='all_users'),

    path('view_distributor/<str:pk>/', views.view_distributor, name='view_distributor'),
    path('view_user/<str:pk>/', views.view_user, name='view_user'),


    #reset password paths start here...
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="website/password_reset.html"),
     name="reset_password"),
    
    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="website/password_reset_sent.html"), 
    name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="website/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="website/password_reset_done.html"), 
        name="password_reset_complete"),
    #reset password paths end here...
        
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)