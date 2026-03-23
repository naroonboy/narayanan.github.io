import json
import yaml
from urllib.parse import urlparse

DEFAULT_TEXT_VAR = "Quarto Resume"

# ✅ Safe helper to avoid None everywhere
def safe(val, default=""):
    return val if val is not None else default

def clean_domain(url):
    if not url:
        return ""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or url  # handle plain domains too
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def pre_render():
    # Load JSON
    with open('RESUME.json', 'r', encoding='utf-8') as json_file:
        meta_data = json.load(json_file)

    # Extract + sanitize values
    google_analytics = meta_data.get("google-analytics")
    title = safe(meta_data.get("title"), "Resume")
    custom_domain_raw = meta_data.get('custom-domain')
    custom_domain = clean_domain(custom_domain_raw)
    secondary_email = safe(meta_data.get('secondary-email'))
    description = safe(meta_data.get('description'), DEFAULT_TEXT_VAR)

    # ✅ Safe keywords (no None)
    keywords_list = [
        secondary_email,
        custom_domain,
        DEFAULT_TEXT_VAR
    ]
    keywords = ', '.join([k for k in keywords_list if k])

    # ✅ Safe email handling
    email_href = f"mailto:{secondary_email}" if secondary_email else ""

    # Build config (NO nulls anywhere)
    development_profile = {
        "website": {
            "site-url": custom_domain or "",  # MUST be string
            "page-footer": {
                "center": [
                    {
                        "text": secondary_email or "Contact",
                        "href": email_href
                    },
                    {
                        "text": "<i>Create your resume</i>",
                        "href": "https://toknow.ai/posts/quarto-resume-template/"
                    },
                ]
            },
        },
        "format": {
            "html": {
                "description": description,
                "output-file": "index.html",  # ✅ ensure homepage
                "header-includes": f'<meta name="keywords" content="{keywords}">',
                "pagetitle": title,
            },
            "pdf": {
                "output-file": "index.pdf"
            }
        }
    }

    # Optional GA
    if google_analytics:
        development_profile["website"]["google-analytics"] = google_analytics

    # Write YAML safely
    with open('_quarto-development.yml', 'w', encoding='utf-8') as yaml_file:
        yaml.dump(development_profile, yaml_file, sort_keys=False, allow_unicode=True)

    print("✅ Created _quarto-development.yml from RESUME.json")

    # Create CNAME if valid
    if custom_domain:
        with open('CNAME', 'w') as cname_file:
            cname_file.write(custom_domain)
        print(f"✅ Created CNAME file with domain: {custom_domain}")


if __name__ == "__main__":
    pre_render()