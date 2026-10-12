import streamlit as st
from generate_data import generate
from brain import index_documents, retrieve, answer, readiness, files

st.set_page_config(page_title='Customer Success Brain', page_icon='🧠', layout='wide')
st.title('🧠 Customer Success Brain')
st.caption('Acme Health · AI assistant launch readiness · Synthetic demonstration data')

if not files():
    generate()
with st.sidebar:
    st.header('Knowledge base')
    st.write(f'{len(files())} synthetic source documents')
    if st.button('Reindex documents'):
        with st.spinner('Indexing documents...'):
            n = index_documents()
        st.success(f'Indexed {n} chunks')
    st.caption('Retrieval uses local ChromaDB embeddings. AI synthesis requires OPENAI_API_KEY.')
    st.header('Source files')
    for path in files():
        with st.expander(path.name):
            st.text(path.read_text(encoding='utf-8'))

st.subheader('Production readiness')
st.error('NO-GO for external production launch — critical controls remain unverified.')
score = readiness()
c1, c2, c3 = st.columns(3)
c1.metric('Critical blockers', sum(x['status']=='BLOCKED' for x in score))
c2.metric('At-risk metrics', sum(x['status']=='AT RISK' for x in score))
c3.metric('Target launch', 'Oct 30')
st.dataframe(score, use_container_width=True, hide_index=True)
st.caption('The scorecard is a transparent, fixed rule-based assessment of the synthetic documents, not a model prediction.')

st.subheader('Ask the customer brain')
question = st.selectbox('Demo question', [
    'Is Acme ready for production? What are the blockers and next steps?',
    'Why does the older green status conflict with the latest evaluation?',
    'What must Ravi, Dr. Kim, and Maya do before the go/no-go review?',
    'Could we launch a restricted internal pilot instead?',
    'Custom question...'
])
if question == 'Custom question...':
    question = st.text_input('Your question', 'What is the biggest customer risk?')
if st.button('Analyze', type='primary') and question.strip():
    with st.spinner('Retrieving evidence and preparing answer...'):
        try:
            sources = retrieve(question, n=7)
            result = answer(question, sources)
            st.markdown(result)
            with st.expander('Retrieved evidence and citations', expanded=True):
                for source in sources:
                    st.markdown(f"**{source['source']}** · distance {source['distance']:.3f}")
                    st.write(source['text'])
        except Exception as exc:
            st.error(f'Analysis failed: {exc}')
            st.info('Try Reindex documents. Confirm dependencies and API key if using AI synthesis.')
