import streamlit as st


# =========================
# 1) CLASS
# =========================
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def subtotal(self, qty):
        return self.price * qty


class Cart:
    def __init__(self):
        self.items = []  # list of tuple: (Product, qty)

    def add_item(self, product, qty):
        self.items.append((product, qty))

    def total(self):
        total_harga = 0
        for product, qty in self.items:
            total_harga += product.subtotal(qty)
        return total_harga

    def receipt_text(self):
        lines = []
        for product, qty in self.items:
            lines.append(f"{product.name} x{qty} = Rp {product.subtotal(qty):,.0f}")
        lines.append("-" * 30)
        lines.append(f"TOTAL = Rp {self.total():,.0f}")
        return "\n".join(lines)


# =========================
# 2) DATA PRODUK (bisa dari dict -> jadi objek Product)
# =========================
catalog = [
    Product("Kopi Hitam", 15000),
    Product("Latte", 25000),
    Product("Roti Bakar", 20000),
    Product("Es Teh", 10000),
]

# Biar gampang dicari berdasarkan nama
catalog_by_name = {p.name: p for p in catalog}


# =========================
# 3) STREAMLIT UI
# =========================
st.title("Kasir Sederhana (Contoh OOP)")

st.write("Pilih menu dan jumlah, lalu klik **Tambah ke Keranjang**.")

# Session state untuk nyimpen cart biar ga reset tiap interaksi
if "cart" not in st.session_state:
    st.session_state.cart = Cart()

col1, col2 = st.columns(2)

with col1:
    nama_produk = st.selectbox("Pilih Produk", list(catalog_by_name.keys()))
with col2:
    qty = st.number_input("Jumlah", min_value=1, value=1, step=1)

if st.button("Tambah ke Keranjang"):
    produk_obj = catalog_by_name[nama_produk]
    st.session_state.cart.add_item(produk_obj, qty)
    st.success(f"{nama_produk} x{qty} ditambahkan!")

st.divider()

# =========================
# 4) TAMPILKAN ISI CART
# =========================
st.subheader("Keranjang")

if len(st.session_state.cart.items) == 0:
    st.info("Keranjang masih kosong.")
else:
    # tampilkan item satu-satu
    for product, qty in st.session_state.cart.items:
        st.write(f"- {product.name} x{qty} = Rp {product.subtotal(qty):,.0f}")

    st.metric("Total Bayar", f"Rp {st.session_state.cart.total():,.0f}")

    # tampilkan versi nota teks
    st.text("NOTA:")
    st.code(st.session_state.cart.receipt_text())


# =========================
# 5) RESET CART
# =========================
if st.button("Reset Keranjang"):
    st.session_state.cart = Cart()
    st.warning("Keranjang direset.")
