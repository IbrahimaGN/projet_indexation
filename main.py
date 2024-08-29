import requests
from bs4 import BeautifulSoup

# URL de base pour les recherches Amazon
base_url = 'https://www.amazon.com/s?k=smartphone&crid=1JJQYWHHZPMGM&sprefix=smart%2Caps%2C266&ref=nb_sb_ss_ts-doa-p_5_5'

# En-têtes pour imiter un navigateur
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept-Language": "en-US,en;q=0.5"
}

def fetch_page(url):
    try:
        # Requête GET
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        return response.content
    except requests.RequestException as e:
        print(f"Erreur lors de la requête : {e}")
        return None

def parse_products(html):
    soup = BeautifulSoup(html, 'html.parser')
    product_elements = soup.find_all('div', {'data-component-type': 's-search-result'})
    products = []

    if not product_elements:
        print("Aucun produit trouvé sur la page.")
    else:
        for product in product_elements:
            title = product.select_one('h2 a span')
            price = product.select_one('span.a-price-whole')
            rating = product.select_one('span.a-icon-alt')
            reviews = product.select_one('span.a-size-base')

            title_text = title.get_text(strip=True) if title else "Titre non disponible"
            price_text = price.get_text(strip=True) if price else "Prix non disponible"
            rating_text = rating.get_text(strip=True) if rating else "Évaluation non disponible"
            reviews_text = reviews.get_text(strip=True) if reviews else "Avis non disponibles"
            
            products.append({
                'Title': title_text,
                'Price': price_text,
                'Rating': rating_text,
                'Reviews': reviews_text
            })
    return products

def main():
    products = []
    page = 1
    max_products = 100

    while len(products) < max_products:
        url = f"{base_url}&page={page}"
        html = fetch_page(url)
        if html is None:
            break

        page_products = parse_products(html)
        if not page_products:
            break

        products.extend(page_products)
        page += 1

        # Arrêter si nous avons atteint le nombre maximum de produits
        if len(products) >= max_products:
            break

    # Afficher les informations des produits récupérés
    for i, product in enumerate(products[:max_products], start=1):
        print(f"Produit {i}:")
        print(f"  Titre: {product['Title']}")
        print(f"  Prix: {product['Price']}")
        print(f"  Évaluation: {product['Rating']}")
        print(f"  Avis: {product['Reviews']}")
        print()

if __name__ == "__main__":
    main()
