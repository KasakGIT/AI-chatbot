import fitz
import requests
from bs4 import BeautifulSoup
import time
import os

# ── 1. Extract PDF ──────────────────────────────────────────
def extract_pdf(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"PDF done: {len(text)} characters saved")

extract_pdf("placement_report_2023_24.pdf", "data/placement_report.txt")

# ── 2. Scrape blogs ─────────────────────────────────────────
def scrape_blog(url, save_path):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    paragraphs = soup.find_all("p")
    text = "\n".join([p.get_text() for p in paragraphs])
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Saved: {save_path} ({len(text)} chars)")

blog_urls = [
    ("https://insightiitb.netlify.app/blog/sharvari", "sharvari_bcg"),
    ("https://insightiitb.netlify.app/blog/dhruv", "dhruv_goldman"),
    ("https://insightiitb.netlify.app/blog/prakriti-shetty", "prakriti_goldman"),
    ("https://insightiitb.netlify.app/blog/ishita", "ishita_barclays"),
    ("https://insightiitb.netlify.app/blog/chaitanya", "chaitanya_deutsche"),
    ("https://insightiitb.netlify.app/blog/vatsal", "vatsal_deshaw"),
    ("https://insightiitb.netlify.app/blog/shrey", "shrey_quadeye"),
    ("https://insightiitb.netlify.app/blog/tanirika", "tanirika_itc"),
    ("https://insightiitb.netlify.app/blog/gautham", "gautham_reckitt"),
    ("https://insightiitb.netlify.app/blog/ammar", "ammar_pg"),
    ("https://insightiitb.netlify.app/blog/aakash", "aakash_axisbank"),
    ("https://insightiitb.netlify.app/blog/swasti", "swasti_idfc"),
    ("https://insightiitb.netlify.app/blog/indrani", "indrayani_indusind"),
    ("https://insightiitb.netlify.app/blog/pranjal-gupta", "pranjal_deutschebank"),
    ("https://insightiitb.netlify.app/blog/achintya", "achintya_consulting"),
    ("https://insightiitb.netlify.app/blog/ananya-shankar-singh", "ananya_pwc"),
    ("https://insightiitb.netlify.app/blog/amolgoel", "amol_bain"),
    ("https://insightiitb.netlify.app/blog/shubhneet", "shubhneet_bcg"),
    ("https://insightiitb.netlify.app/blog/muskaan-chandra", "muskaan_datascience"),
    ("https://insightiitb.netlify.app/blog/kunind-sahu", "kunind_amex"),
    ("https://insightiitb.netlify.app/blog/unnatee-pawar", "unnatee_unacademy"),
    ("https://insightiitb.netlify.app/blog/tejas", "tejas_optiver"),
    ("https://insightiitb.netlify.app/blog/dhruv-arora", "dhruv_optiver"),
    ("https://insightiitb.netlify.app/blog/aadish", "aadish_quadeye"),
    ("https://insightiitb.netlify.app/blog/prerna", "prerna_bajaj"),
    ("https://insightiitb.netlify.app/blog/nirmal", "nirmal_mitacs"),
    ("https://insightiitb.netlify.app/blog/abeer", "abeer_mitacs"),
    ("https://insightiitb.netlify.app/blog/shreya", "shreya_purdue"),
    ("https://insightiitb.netlify.app/blog/isha-mukherjee", "isha_gulfstream"),
    ("https://insightiitb.netlify.app/blog/advait", "advait_ubc"),
    ("https://insightiitb.netlify.app/blog/rudraksh", "rudraksh_airbus"),
    ("https://insightiitb.netlify.app/blog/shivam", "shivam_jlr"),
    ("https://insightiitb.netlify.app/blog/mehul", "mehul_ti"),
    ("https://insightiitb.netlify.app/blog/tanmay-joshi", "tanmay_google"),
    ("https://insightiitb.netlify.app/blog/jai-jobanputra", "jai_atomberg"),
    ("https://insightiitb.netlify.app/blog/malavika", "malavika_indiana"),
    ("https://insightiitb.netlify.app/blog/oshin", "oshin_tata"),
    ("https://insightiitb.netlify.app/blog/soham", "soham_toronto"),
    ("https://insightiitb.netlify.app/blog/amitkumarmallik", "amit_braunschweig"),
    ("https://insightiitb.netlify.app/blog/harshada", "harshda_heidelberg"),
    ("https://insightiitb.netlify.app/blog/harshit", "harshit_cibil"),
    ("https://insightiitb.netlify.app/blog/sanidhya", "sanidhya_wien"),
    ("https://insightiitb.netlify.app/blog/bhuvan", "bhuvan_daikin"),
    ("https://insightiitb.netlify.app/blog/sharvaree-sinkar", "sharvaree_wellsfargo"),
    ("https://insightiitb.netlify.app/blog/anishsatpati", "anish_siemens"),
]

for url, name in blog_urls:
    try:
        scrape_blog(url, f"data/blogs/{name}.txt")
        time.sleep(1)
    except Exception as e:
        print(f"Failed {name}: {e}")

print("\nDone! Files in data/:")
print(os.listdir("data"))
print("Blogs scraped:", len(os.listdir("data/blogs")))