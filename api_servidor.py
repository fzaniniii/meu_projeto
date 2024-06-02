from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import logging

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

logging.basicConfig(level=logging.DEBUG)

@app.route('/executar_pesquisa', methods=['POST'])
def executar_pesquisa():
    try:
        data = request.get_json()
        palavras_chave = data.get('palavras_chave', [])
        opcao = data.get('opcao', 'trending')

        if opcao == 'trending':
            logging.debug(f"Trending option selected with keywords: {palavras_chave}")
            pytrends.build_payload(palavras_chave, cat=0, timeframe='today 12-m', geo='', gprop='')
            data = pytrends.interest_over_time()
            if not data.empty:
                data = data.reset_index().to_dict(orient='records')
            else:
                data = []
        elif opcao == 'interest_by_region':
            logging.debug(f"Interest by region option selected with keywords: {palavras_chave}")
            pytrends.build_payload(palavras_chave, cat=0, timeframe='today 12-m', geo='', gprop='')
            data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
            if not data.empty:
                data = data.reset_index().to_dict(orient='records')
            else:
                data = []
        elif opcao == 'related_queries':
            logging.debug(f"Related queries option selected with keywords: {palavras_chave}")
            pytrends.build_payload(palavras_chave, cat=0, timeframe='today 12-m', geo='', gprop='')
            related_queries = pytrends.related_queries()
            data = {kw: related_queries[kw]['top'].to_dict('records') if related_queries[kw]['top'] is not None else [] for kw in related_queries}
        elif opcao == 'related_topics':
            logging.debug(f"Related topics option selected with keywords: {palavras_chave}")
            pytrends.build_payload(palavras_chave, cat=0, timeframe='today 12-m', geo='', gprop='')
            related_topics = pytrends.related_topics()
            data = {kw: related_topics[kw]['rising'].to_dict('records') if related_topics[kw]['rising'] is not None else [] for kw in related_topics}
        else:
            return jsonify({"erro": "Opção inválida"}), 400

        return jsonify(data), 200

    except Exception as e:
        logging.error(f"Error during execution: {str(e)}")
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
