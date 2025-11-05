from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from .models import User, Category, Listing, Comments, Bid

# Configuration du titre et des en-têtes de l'interface admin
admin.site.site_header = "CommerceHub Administration"
admin.site.site_title = "CommerceHub Admin"
admin.site.index_title = "Panneau d'Administration"

# Configuration personnalisée pour l'utilisateur
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'watching_count')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    def watching_count(self, obj):
        return obj.watching_listings.count()
    watching_count.short_description = 'Items en Watchlist'

# Configuration pour les catégories
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('categoryName', 'listing_count')
    search_fields = ('categoryName',)
    ordering = ('categoryName',)
    
    def listing_count(self, obj):
        return obj.category.count()
    listing_count.short_description = 'Nombre d\'annonces'

# Configuration pour les enchères/offres
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bid', 'listing_title', 'created_date')
    list_filter = ('bid', 'user')
    search_fields = ('user__username', 'bid')
    ordering = ('-id',)
    readonly_fields = ('created_date',)
    
    def listing_title(self, obj):
        # Trouve l'annonce liée à cette enchère
        listing = Listing.objects.filter(price=obj).first()
        return listing.title if listing else "Non assigné"
    listing_title.short_description = 'Annonce'
    
    def created_date(self, obj):
        # Si vous ajoutez un champ date plus tard
        return "N/A"
    created_date.short_description = 'Date de création'

# Configuration pour les annonces
@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'current_price', 'isActive', 'watchlist_count', 'comments_count')
    list_filter = ('isActive', 'category', 'owner')
    search_fields = ('title', 'description', 'owner__username')
    ordering = ('-id',)
    readonly_fields = ('watchlist_count', 'comments_count')
    
    # Organisez les champs dans l'interface d'édition
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'description', 'imageUrl')
        }),
        ('Prix et Enchères', {
            'fields': ('price',)
        }),
        ('Catégorie et Propriétaire', {
            'fields': ('category', 'owner')
        }),
        ('Statut', {
            'fields': ('isActive',)
        }),
        ('Watchlist', {
            'fields': ('watchlist',),
            'classes': ('collapse',)
        }),
        ('Statistiques', {
            'fields': ('watchlist_count', 'comments_count'),
            'classes': ('collapse',)
        })
    )
    
    filter_horizontal = ('watchlist',)  # Interface plus conviviale pour ManyToMany
    
    def current_price(self, obj):
        return f"{obj.price.bid}€" if obj.price else "Aucun prix"
    current_price.short_description = 'Prix actuel'
    
    def watchlist_count(self, obj):
        return obj.watchlist.count()
    watchlist_count.short_description = 'Personnes qui suivent'
    
    def comments_count(self, obj):
        return obj.listingComment.count()
    comments_count.short_description = 'Nombre de commentaires'

# Configuration pour les commentaires
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'listing_title', 'message_preview', 'created_date')
    list_filter = ('author', 'listing')
    search_fields = ('message', 'author__username', 'listing__title')
    ordering = ('-id',)
    readonly_fields = ('created_date',)
    
    # Organisez les champs
    fields = ('author', 'listing', 'message', 'created_date')
    
    def listing_title(self, obj):
        return obj.listing.title if obj.listing else "Aucune annonce"
    listing_title.short_description = 'Annonce'
    
    def message_preview(self, obj):
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Aperçu du message'
    
    def created_date(self, obj):
        # Si vous ajoutez un champ date plus tard
        return "N/A"
    created_date.short_description = 'Date de création'

# Classe d'administration personnalisée avec statistiques
class CommerceAdminSite(AdminSite):
    site_header = "CommerceHub Administration"
    site_title = "CommerceHub Admin"
    index_title = "Panneau d'Administration"

    def index(self, request, extra_context=None):
        """
        Affiche le tableau de bord avec des statistiques personnalisées
        """
        extra_context = extra_context or {}
        
        # Statistiques générales
        extra_context.update({
            'listings_count': Listing.objects.count(),
            'users_count': User.objects.count(),
            'bids_count': Bid.objects.count(),
            'comments_count': Comments.objects.count(),
            'recent_listings': Listing.objects.order_by('-id')[:5],
            'recent_comments': Comments.objects.order_by('-id')[:5],
        })
        
        return super().index(request, extra_context)

# Remplacer le site d'administration par défaut
admin_site = CommerceAdminSite(name='commercehub_admin')

# Enregistrer les modèles avec leurs configurations personnalisées
admin_site.register(User, CustomUserAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Listing, ListingAdmin)
admin_site.register(Comments, CommentsAdmin)
admin_site.register(Bid, BidAdmin)

# Aussi garder l'enregistrement par défaut pour compatibilité
admin.site.register(User, CustomUserAdmin)




