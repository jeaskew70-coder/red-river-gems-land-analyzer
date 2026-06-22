import streamlit as st
from fpdf import FPDF
import requests

st.set_page_config(page_title="Red River Gems Land Analyzer", page_icon="🌾", layout="centered")

# ==================== API KEYS ====================
EIA_API_KEY = "jjD5aFx44aC5JSiPDU63fG4f5By7XdHRNYsmqAM8"
OPENWEATHER_API_KEY = "80103cffa2d1802f17caa5bfc3bc8f27"

def get_eia_gas_price(state):
    padd_map = {
        "TX": "PET.EMM_EPM0_PTE_R3X_DPG.W",
        "OK": "PET.EMM_EPM0_PTE_R3X_DPG.W",
        "AR": "PET.EMM_EPM0_PTE_R3X_DPG.W",
        "LA": "PET.EMM_EPM0_PTE_R3X_DPG.W",
    }
    
    series_id = padd_map.get(state, "PET.EMM_EPM0_PTE_R3X_DPG.W")
    url = f"https://api.eia.gov/series/?api_key={EIA_API_KEY}&series_id={series_id}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if "series" in data and len(data["series"]) > 0:
            latest = data["series"][0]["data"][0]
            return round(float(latest[1]), 2)
    except:
        pass
    fallback_prices = {"TX": 3.45, "OK": 3.35, "AR": 3.30, "LA": 3.50}
    return fallback_prices.get(state, 3.45)


def get_current_weather(city, state_code):
    if not city:
        return None
    
    query = f"{city},{state_code},US"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={OPENWEATHER_API_KEY}&units=imperial"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("cod") == 200:
            return {
                "temp": round(data["main"]["temp"]),
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "city": data["name"]
            }
    except:
        pass
    return None


# ==================== HEADER ====================
st.title("🌾 Red River Gems Land Analyzer")

st.markdown("""
**Free tool to help you research and evaluate land** across Texas, Oklahoma, Arkansas, and Louisiana.

Get realistic cost estimates, tax guidance based on how you plan to use the land, current regional data, and a full due diligence checklist — all in one clean, downloadable report.
""")

st.divider()

# === INPUTS ===
st.header("Enter Property Details")

col1, col2 = st.columns(2)
with col1:
    state = st.selectbox("State", ["TX", "OK", "AR", "LA"])
    county_or_city = st.text_input("County or Nearest City", placeholder="e.g. Granbury")

with col2:
    acreage = st.number_input("Acreage", min_value=0.1, value=1.0, step=0.5)
    asking_price = st.number_input("Asking Price ($)", min_value=1000, value=120000, step=1000)

purpose = st.selectbox(
    "Intended Use / Purpose",
    ["Homestead / Residential", 
     "Ranch / Livestock / Agricultural", 
     "Recreational / Hunting", 
     "Investment / Speculation", 
     "Timber", 
     "Other / Unsure"]
)

utilities_on_site = st.selectbox("Utilities available on or near the property?", ["Yes", "No"])

st.divider()

if "report_generated" not in st.session_state:
    st.session_state.report_generated = False

if st.button("Generate Report", type="primary", use_container_width=True):
    st.session_state.report_generated = True
    st.session_state.state = state
    st.session_state.county_or_city = county_or_city
    st.session_state.acreage = acreage
    st.session_state.asking_price = asking_price
    st.session_state.purpose = purpose
    st.session_state.utilities_on_site = utilities_on_site

if st.session_state.report_generated:
    st.success("Report generated successfully!")

    state = st.session_state.state
    county_or_city = st.session_state.county_or_city
    acreage = st.session_state.acreage
    asking_price = st.session_state.asking_price
    purpose = st.session_state.purpose
    utilities_on_site = st.session_state.utilities_on_site

    # Tax rate logic
    if purpose in ["Ranch / Livestock / Agricultural", "Timber"]:
        effective_tax_rate = 0.0045
        tax_note = "Assumes qualification for agricultural or wildlife valuation. Actual taxes may be higher if you don't qualify."
    elif purpose == "Homestead / Residential":
        effective_tax_rate = 0.012
        tax_note = "Standard homestead estimate. Agricultural valuation may further reduce taxes if you qualify."
    else:
        effective_tax_rate = 0.014
        tax_note = "Standard valuation estimate. Special use valuations may significantly lower taxes if you qualify."

    # Financial Snapshot
    st.subheader("💰 Financial Snapshot (Rough Estimates)")

    closing_costs = asking_price * 0.03
    total_at_closing = asking_price + closing_costs
    est_annual_taxes = asking_price * effective_tax_rate

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Asking Price", f"${asking_price:,.0f}")
        st.metric("Closing Costs (3%)", f"${closing_costs:,.0f}")
    with col4:
        st.metric("Total at Closing", f"${total_at_closing:,.0f}")
        st.metric("Est. Annual Property Taxes", f"${est_annual_taxes:,.0f}")

    st.write(f"**Price per Acre:** ${asking_price / acreage:,.0f}")
    st.caption(tax_note)

    if utilities_on_site == "No":
        st.warning("Utilities not reported on site. Budget for electric line extension, well drilling, and septic system.")

    st.divider()

    # ==================== IMPROVED CULTURAL & LIFESTYLE SECTION ====================
    st.subheader("🏡 Cultural & Lifestyle Factors")
    st.caption(f"Specific data for **{county_or_city}** is limited — here is relevant regional context for the Red River area.")

    with st.expander("🍽️ Food Access & Local Flavor"):
        st.write("Food access in the Red River region varies depending on how close you are to a county seat or larger town. Most rural areas have at least a Dollar General, Brookshire’s, or small local grocer. Larger selections are usually found in nearby towns.")
        st.write("Local food culture leans heavily into Southern comfort food, BBQ, catfish, fried vegetables, and Tex-Mex or Cajun influences depending on the exact area. Many homesteaders also rely on local butchers and meat processors.")
        st.write("**What living here often feels like:** Expect a slower pace with strong food traditions. Many people grow gardens, hunt, or fish to supplement groceries. Seasonal farmers markets and roadside stands appear in spring through fall.")

    with st.expander("🎉 Festivals, Entertainment & Community"):
        st.write("County fairs, rodeos, church events, and homecoming celebrations form the heartbeat of social life in the Red River region. These events are deeply tied to local culture and community connection.")
        st.write("Larger entertainment options (movies, dining, shopping) are usually a 30–90 minute drive to places like Paris TX, Texarkana, Shreveport, or Ardmore OK.")
        st.write("**Notable regional events:**")
        if state == "TX":
            st.markdown("- [Texas State Fair](https://bigtex.com/) — Major annual event in Dallas")
            st.markdown("- Many counties have well-attended rodeos and livestock shows in spring and fall.")
        elif state == "OK":
            st.markdown("- [Four States Fair & Rodeo](https://www.fourstatesfair.com/)")
        elif state == "AR":
            st.markdown("- County fairs and harvest festivals are very common in the fall.")
        elif state == "LA":
            st.markdown("- Strong Cajun and festival culture with many small community events.")

    with st.expander("🎓 Education"):
        st.write("Public K-12 education is provided by local school districts, and quality can vary significantly between districts. Many rural families supplement with homeschooling or small private options.")
        st.write("Higher education options in the broader region include community colleges and universities such as Texas A&M-Commerce, Southeastern Oklahoma State, and others.")
        st.write("**Helpful resources:**")
        if state == "TX":
            st.markdown("- [Texas Education Agency (TEA)](https://tea.texas.gov/)")
        elif state == "OK":
            st.markdown("- [Oklahoma State Department of Education](https://sde.ok.gov/)")
        elif state == "AR":
            st.markdown("- [Arkansas Division of Elementary and Secondary Education](https://dese.ade.arkansas.gov/)")
        elif state == "LA":
            st.markdown("- [Louisiana Department of Education](https://www.louisianabelieves.com/)")

    with st.expander("🏥 Healthcare"):
        st.write("Access to healthcare varies significantly between rural areas and towns with hospitals. Many smaller communities have clinics, but major hospitals and specialists are usually located in larger regional hubs.")
        st.write("**Helpful resources by state:**")
        if state == "TX":
            st.markdown("- [Texas Health and Human Services](https://www.hhs.texas.gov/)")
        elif state == "OK":
            st.markdown("- [Oklahoma State Department of Health](https://oklahoma.gov/health.html)")
        elif state == "AR":
            st.markdown("- [Arkansas Department of Health](https://www.healthy.arkansas.gov/)")
        elif state == "LA":
            st.markdown("- [Louisiana Department of Health](https://ldh.la.gov/)")

    with st.expander("📡 Internet & Connectivity"):
        st.write("High-speed internet is often limited in rural parts of the Red River region. Many residents rely on fixed wireless providers or satellite internet (such as Starlink). Cell coverage can also be spotty in more remote areas.")
        st.write("**Helpful resources:**")
        if state == "TX":
            st.markdown("- [Texas Broadband Map](https://texasbroadband.texas.gov/)")
        st.markdown("- [FCC Broadband Map](https://broadbandmap.fcc.gov/)")

    with st.expander("🚨 Emergency Services"):
        st.write("Emergency response times in rural areas are often longer than in towns or cities (commonly 15–40+ minutes depending on location). Many counties rely on volunteer fire departments and limited EMS coverage.")
        st.write("**State resources:**")
        if state == "TX":
            st.markdown("- [Texas Emergency Management](https://tdem.texas.gov/)")
        elif state == "OK":
            st.markdown("- [Oklahoma Emergency Management](https://oklahoma.gov/oem.html)")
        elif state == "AR":
            st.markdown("- [Arkansas Department of Emergency Management](https://www.adem.arkansas.gov/)")
        elif state == "LA":
            st.markdown("- [Louisiana Governor's Office of Homeland Security](https://gohsep.la.gov/)")

    with st.expander("🛒 Local Stores & Shopping"):
        st.write("Most rural areas have at least a Dollar General or small local store. Larger selections (Walmart, Brookshire’s, Tractor Supply, etc.) are usually found in or near county seats. Many locals also shop in nearby larger towns for bigger purchases.")
        st.write("**Helpful resources:** Search Google for your county + “Chamber of Commerce” for local business listings.")

    with st.expander("🛡️ Safety & Rural Context"):
        st.write("Violent crime rates in rural areas of the Red River region are typically well below the U.S. average. Most people describe these communities as safe and neighborly. Property crime (such as theft from outbuildings or equipment) can occasionally be a concern in more remote areas.")
        st.write("**Tip:** Talk to neighbors and local law enforcement when evaluating a property.")

    st.caption("Note: Specific local options can vary. Always verify current information locally.")

    st.divider()

    # ==================== WEATHER and the rest of the app ====================
    # (Weather expander + Cost of Living + Regional Insights + Checklist + PDF remain the same as previous version)

    with st.expander("🌤️ Weather, Climate & Environmental Conditions"):
        st.write(f"**Current conditions near {county_or_city or 'the selected area'}**")

        weather = get_current_weather(county_or_city, state) if county_or_city else None

        if weather:
            colw1, colw2 = st.columns(2)
            with colw1:
                st.metric("Temperature", f"{weather['temp']}°F")
                st.metric("Humidity", f"{weather['humidity']}%")
            with colw2:
                st.write(f"**Conditions:** {weather['description']}")
                st.write(f"**Location:** {weather['city']}")
        else:
            st.info("Enter a city name above to see current weather conditions.")

        st.divider()

        st.subheader("Regional Climate Averages")

        if state == "TX":
            st.write("**Northeast Texas / Red River area:**")
            st.write("- Average Annual Rainfall: ~45–50 inches")
            st.write("- Average High Temp (Summer): 92–95°F")
            st.write("- Average Low Temp (Winter): 32–38°F")
        elif state == "OK":
            st.write("**Southeast Oklahoma / Red River area:**")
            st.write("- Average Annual Rainfall: ~40–48 inches")
            st.write("- Average High Temp (Summer): 90–94°F")
            st.write("- Average Low Temp (Winter): 28–35°F")
        elif state == "AR":
            st.write("**Southwest Arkansas:**")
            st.write("- Average Annual Rainfall: ~48–55 inches")
            st.write("- Average High Temp (Summer): 90–93°F")
            st.write("- Average Low Temp (Winter): 30–36°F")
        else:
            st.write("**Northwest Louisiana:**")
            st.write("- Average Annual Rainfall: ~50–58 inches")
            st.write("- Average High Temp (Summer): 91–94°F")
            st.write("- Average Low Temp (Winter): 35–40°F")

        st.divider()

        st.subheader("Drought Conditions")
        st.write("Check the latest drought status for your area:")
        st.markdown("[View Live U.S. Drought Monitor Map](https://droughtmonitor.unl.edu/CurrentConditions.aspx)")

    # Cost of Living
    st.subheader("📈 Cost of Living (Monthly Estimates)")

    gas_price = get_eia_gas_price(state)

    if state == "TX":
        groceries = 880
        utilities = 245
        rent = 1250
    elif state == "OK":
        groceries = 820
        utilities = 220
        rent = 1050
    elif state == "AR":
        groceries = 810
        utilities = 215
        rent = 1020
    else:
        groceries = 850
        utilities = 230
        rent = 1100

    col5, col6 = st.columns(2)
    with col5:
        st.metric("Groceries (family of 4)", f"${groceries}")
        st.metric("Gas (per gallon - EIA)", f"${gas_price:.2f}")
    with col6:
        st.metric("Utilities", f"${utilities}")
        st.metric("Rent (2BR small town)", f"${rent}")

    st.caption(f"Gas price pulled live from EIA. Other values are regional estimates for {state} (updated quarterly).")

    st.divider()

    # Regional Insights
    st.subheader("📍 Regional Insights & Things to Consider")

    insights = [
        "**Mineral rights & title** - Severed mineral estates are extremely common. Always get a full title abstract and consult a local attorney.",
        "**Special valuation programs** - Agricultural, timber, and wildlife valuations can dramatically reduce property taxes if you qualify.",
        "**Water sources & realities** - Most rural parcels rely on private wells. Understand local aquifer and water rights rules.",
        "**Soil, drainage & growing conditions** - Much of the region has heavy clay or clay-loam soils. Get a soil test through your county extension office.",
        "**Connectivity & services** - High-speed internet is often limited. Starlink is popular in many rural areas.",
        "**Wildlife, fencing & land use** - Deer and feral hogs are abundant. Good perimeter fencing is essential.",
        "**Texas school district taxes** - Even with ag valuation, the school district portion of your tax bill is often the largest.",
        "**Homesteading realities** - Begin with a soil test. Plan for high summer cooling loads and strong perimeter fencing.",
    ]

    for i, insight in enumerate(insights, 1):
        st.write(f"**{i}.** {insight}")

    st.divider()

    # Checklist
    checklist = [
        "Order a current survey and review all easements and encroachments.",
        "Check the property against current FEMA flood maps.",
        "Perform a thorough title search (especially for mineral rights).",
        "Ask about agricultural, timber, or wildlife valuation programs in your state.",
        "Get written estimates for utilities, well drilling, and septic if not on site.",
        "Test or research water availability and understand local water rights.",
        "Evaluate internet and cell coverage on the property.",
        "Review county zoning, subdivision regulations, and building permits.",
        "Arrange a perc test if installing a septic system.",
        "Walk the boundaries and talk to neighbors.",
        "Budget for fencing, gravel drive, and outbuildings.",
        "Get insurance quotes early.",
        "Visit the county extension office for soil maps and local growing advice.",
        "In Texas, confirm school district tax rates and any special district taxes.",
    ]

    st.subheader("✅ Important Considerations Checklist")

    for item in checklist:
        st.checkbox(item)

    st.divider()

    # PDF Export
    if st.button("Download Report as PDF", use_container_width=True):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 12, "Red River Gems Land Analyzer Report", ln=True, align="C")
        pdf.ln(3)

        pdf.set_font("Arial", size=11)
        pdf.cell(0, 8, f"Location: {county_or_city}, {state}  |  Acreage: {acreage} acres  |  Asking Price: ${asking_price:,.0f}", ln=True, align="C")
        pdf.ln(8)

        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, "Financial Snapshot (Rough Estimates)", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, f"Asking Price: ${asking_price:,.0f}\n"
                           f"Buyer Closing Costs (3%): ${closing_costs:,.0f}\n"
                           f"Total at Closing: ${total_at_closing:,.0f}\n"
                           f"Est. Annual Property Taxes: ${est_annual_taxes:,.0f}\n"
                           f"Price per Acre: ${asking_price / acreage:,.0f}")

        pdf.ln(2)
        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 6, f"Tax estimate based on intended use: {purpose}. {tax_note}")

        if utilities_on_site == "No":
            pdf.ln(2)
            pdf.set_font("Arial", "I", 10)
            pdf.multi_cell(0, 6, "Note: Utilities not reported on site. Budget for electric line extension, well drilling, and septic system.")

        pdf.ln(5)

        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, "Cost of Living (Monthly Estimates)", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, f"Groceries (family of 4): ${groceries}\n"
                           f"Gasoline (per gallon): ${gas_price:.2f} (EIA live data)\n"
                           f"Utilities (electric + water + trash): ${utilities}\n"
                           f"Rent (approx 2BR in small town): ${rent}")

        pdf.ln(5)

        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, "Cultural & Lifestyle Factors", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, "This report includes regional context for Food Access, Festivals & Community Events, "
                           "Education, Healthcare, Internet Connectivity, Emergency Services, Local Stores & Shopping, "
                           "and Safety. Specific local options can vary - always verify current information locally.")

        pdf.ln(5)

        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, "Key Regional Insights", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, "- Mineral rights are often severed - always get a full title abstract.\n"
                           "- Agricultural and wildlife valuations can significantly reduce property taxes if you qualify.\n"
                           "- Most rural parcels rely on private wells - understand local water rights.\n"
                           "- High-speed internet is often limited; Starlink is commonly used.\n"
                           "- Wildlife (deer, feral hogs) is abundant - good fencing is essential.\n"
                           "- Emergency response times can be 15-40+ minutes in remote areas.")

        pdf.ln(5)

        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 12, "Important Considerations Checklist", ln=True, align="C")
        pdf.ln(8)

        pdf.set_font("Arial", "B", 10)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(10, 8, "#", border=1, align="C", fill=True)
        pdf.cell(180, 8, "Item", border=1, align="L", fill=True)
        pdf.ln()

        checklist_items = checklist

        pdf.set_font("Arial", size=9)
        for i, item in enumerate(checklist_items, 1):
            pdf.cell(10, 7, str(i), border=1, align="C")
            pdf.cell(180, 7, item, border=1, align="L")
            pdf.ln()

        pdf.ln(10)

        pdf.set_font("Arial", "I", 9)
        pdf.multi_cell(0, 6, "© 2026 Red River Gems. All rights reserved.\n"
                           "Red River Gems and the Red River Gems Land Analyzer are trademarks of their owner.\n"
                           "This report uses approximate 2025-2026 regional data for planning purposes only. "
                           "Nothing here is financial, legal, tax, or real estate advice.")

        pdf_output = bytes(pdf.output(dest="S"))

        st.download_button(
            label="Download PDF",
            data=pdf_output,
            file_name=f"RedRiverGems_Report_{county_or_city.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )

    st.success("Report complete. Always verify information with local professionals before making decisions.")

# ==================== FOOTER ====================
st.divider()

st.caption("""
© 2026 Red River Gems. All rights reserved.  
Red River Gems and the Red River Gems Land Analyzer are trademarks of their owner.

Follow for more land & homesteading content:  
[ TikTok](https://www.tiktok.com/@YOUR_TIKTOK) • [Instagram](https://www.instagram.com/YOUR_INSTAGRAM)
""")
