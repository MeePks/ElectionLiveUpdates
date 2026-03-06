import streamlit as st
import pandas as pd
import time

# ------------------ Page Config ------------------
st.set_page_config(page_title="Nepal Election Live", layout="wide")

# ------------------ CSS Styling ------------------
st.markdown("""
<style>

body{
    background-color:#0f172a;
    color:white;
    font-family:sans-serif;
}

.chetra-box{
    background-color:#1e293b;
    border-radius:15px;
    padding:10px;
    margin-bottom:15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

.leader{
    border:3px solid;
    animation: flash 1s infinite;
    border-radius:10px;
    padding:5px;
}

@keyframes flash{
    0%{box-shadow:0 0 10px;}
    50%{box-shadow:0 0 25px;}
    100%{box-shadow:0 0 10px;}
}

.candidate{
    text-align:center;
    margin:5px;
}

.vote{
    font-size:20px;
    font-weight:bold;
    color:white;
}

.party-table th, .party-table td {
    padding:8px;
    text-align:center;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ------------------ Title & Flag ------------------
# Use two columns: left = title + flag, right = party tally
top_cols = st.columns([3,1])
with top_cols[0]:
    st.title("🇳🇵 Nepal Live Election Results")
    st.image("Flag_of_Nepal.gif", width=120)

# Placeholder for party tally
party_placeholder = top_cols[1].empty()

# Placeholder for main chetra grid
grid_placeholder = st.empty()

# ------------------ Main Loop ------------------
while True:

    # Load data
    df = pd.read_csv("results.csv")
    party_tally = pd.read_csv("party_tally.csv")

    # ------------------ Party Tally ------------------
    with party_placeholder.container():
        st.subheader("Party Leads & Wins")
        party_display = party_tally.copy()
        party_display = party_display[["Party","leads","wins"]]
        #st.table(party_display.reset_index(drop=True).style.set_properties(**{'background-color':"#01affa",'color':'white'}))
        st.dataframe(
            party_display.style.set_properties(
                **{
                    "background-color": "#1e293b",
                    "color": "white",
                    "text-align": "center"
                }
            ),
            hide_index=True
            #,
            #width=300,
            #height=200
        )
    # ------------------ Chetra Grid ------------------
    with grid_placeholder.container():

        chetras = sorted(df['chetra'].unique())
        # Make 3 chetras per row
        rows = [chetras[i:i+3] for i in range(0,len(chetras),3)]

        for row_chetras in rows:
            cols = st.columns(3)
            for i,ch in enumerate(row_chetras):
                with cols[i]:
                    st.markdown('<div class="chetra-box">', unsafe_allow_html=True)
                    st.subheader(f"{ch}")

                    chetra_df = df[df['chetra']==ch]
                    # Top 2 candidates
                    top2 = chetra_df.sort_values("votes", ascending=False).head(2)
                    leader_votes = top2.iloc[0]['votes']

                    candidate_cols = st.columns(len(top2))
                    for j, (_, r) in enumerate(top2.iterrows()):
                        with candidate_cols[j]:
                            leader_class = "leader" if r['votes']==leader_votes else ""
                            st.markdown(f'<div class="{leader_class}" style="border-color:{r["color"] if r["votes"]==leader_votes else "white"};">', unsafe_allow_html=True)
                            st.image(r['symbol'], width=60)
                            st.markdown(f"<h3 style='text-align:left'>{r['candidate']}</h3>", unsafe_allow_html=True)
                            st.markdown(f"<h3 style='text-align:left'>{r['votes']}</h3>", unsafe_allow_html=True)
                            st.markdown(f'<div class="vote">{r["votes"]}</div>', unsafe_allow_html=True)

                            # Progress bar using party color
                            progress = r['votes'] / leader_votes
                            st.progress(progress)

                            # Swing indicator
                            swing = leader_votes - r['votes']
                            if swing > 0:
                                st.write(f"Trailing by {swing}")
                            else:
                                st.write("Leading")

                            st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown('</div>', unsafe_allow_html=True)

    # Refresh every 3 seconds
    time.sleep(3)