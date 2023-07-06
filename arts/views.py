from django.shortcuts import render, redirect
from .forms import ArtworkForm, ContactForm
from django.core.mail import send_mail
from .models import Artwork
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect

def upload_artwork(request):
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gallery')
    else:
        form = ArtworkForm()
    return render(request, 'upload.html', {'form': form})

def gallery(request):
    artworks = Artwork.objects.all()
    form = ArtworkForm()
    if not artworks:
        return render(request, 'gallery.html', {'artworks': artworks, 'form': form, 'no_artworks': True})
    return render(request, 'gallery.html', {'artworks': artworks, 'form': form})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']


            send_mail(
                subject,
                f"Name: {name}\nEmail: {email}\n\n{message}",
                email,
                ['maria.zanescu@gmail.com'],
                fail_silently=True,
            )
            return render(request, 'contact_success.html')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})

def search(request):
    query = request.GET.get('query')
    search_results = []

    if query:
        search_results = Artwork.objects.filter(
            Q(title__icontains=query)
        )

    return render(request, 'search_results.html', {'query': query, 'search_results': search_results})

def share_facebook(request, artwork_id):
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    share_url = request.build_absolute_uri(artwork.image.url)
    facebook_url = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
    return redirect(facebook_url)

def share_twitter(request, artwork_id):
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    share_url = request.build_absolute_uri(artwork.image.url)
    artwork_title = artwork.title
    twitter_url = f"https://twitter.com/intent/tweet?url={share_url}&text=Check out this artwork: {artwork_title}"
    return redirect(twitter_url)