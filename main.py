import osmnx as ox
import networkx as nx
import folium

# بارگیری نقشه خیابان‌های تهران
G = ox.graph_from_place('Tehran, Iran', network_type='drive')

# تعریف مختصات شهرک غرب و مولوی
shahrak_gharab_coords = (35.7805, 51.3654)  # مختصات تقریبی شهرک غرب
mowlavi_coords = (35.6750, 51.4250)  # مختصات تقریبی مولوی

# پیدا کردن نزدیک‌ترین گره‌ها به مختصات ورودی
origin_node = ox.nearest_nodes(G, X=shahrak_gharab_coords[1], Y=shahrak_gharab_coords[0])
destination_node = ox.nearest_nodes(G, X=mowlavi_coords[1], Y=mowlavi_coords[0])

# پیدا کردن کوتاه‌ترین مسیر
shortest_route = nx.shortest_path(G, origin_node, destination_node, weight='length')

# ایجاد نقشه پایه با Folium
m = folium.Map(location=shahrak_gharab_coords, zoom_start=12)

# اضافه کردن مسیر به نقشه
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_route]
folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)

# اضافه کردن نشانگر برای مبدا و مقصد
folium.Marker(location=shahrak_gharab_coords, popup="Shahrak Gharb", icon=folium.Icon(color="green")).add_to(m)
folium.Marker(location=mowlavi_coords, popup="Mowlavi", icon=folium.Icon(color="red")).add_to(m)

# ایجاد گزارش از مسیر
report = []

# افزودن اطلاعات خلاصه برای گام به گام مسیر
report.append(f"شروع از: {shahrak_gharab_coords[0]}, {shahrak_gharab_coords[1]} (شهرک غرب)")

# برای جلوگیری از تکرار خیابان‌ها، خیابان‌های قبلی را ذخیره می‌کنیم
last_street_name = None

# تغییرات جدید برای به‌روز کردن گزارش
for i, (u, v) in enumerate(zip(shortest_route[:-1], shortest_route[1:])):
    # گرفتن نام خیابان از یال
    edge_data = G.get_edge_data(u, v)
    print(edge_data)
    if 'name' in edge_data[0]:  # اگر نام خیابان موجود باشد
        name = edge_data[0]['name']

        if isinstance(name, list):
            name = ', '.join(name)  # تبدیل لیست به رشته

        # اگر نام خیابان جدید باشد و با خیابان قبلی متفاوت است
        if name != last_street_name:
            # اگر این خیابان قبلاً گزارش شده نباشد
            if last_street_name is not None:
                # ثبت انتقال از خیابان قبلی به خیابان جدید
                report.append(f"از  {last_street_name} به  {name} بروید.")
            last_street_name = name  # به روز رسانی خیابان آخرین

# گزارش به انتها
report.append(f"از  {last_street_name} به مقصد خواهید رسید.")

# ذخیره گزارش در یک فایل متنی
with open("route_report_summary.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(report))

# نمایش نقشه
m.save("shortest_route_map_with_street_names.html")
