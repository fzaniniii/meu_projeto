from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/executar_pesquisa', methods=['POST'])
def executar_pesquisa():
    data = request.get_json()
    palavras_chave = data.get('palavras_chave', [])
    opcao = data.get('opcao', 'trending')

    if opcao == 'trending':
        pytrends.build_payload(palavras_chave, cat=0, timeframe='today 12-m', geo='', gprop='')
        data = pytrends.interest_over_time()
        if not data.empty:
            data = data.reset_index().to_dict(orient='records')
        else:
            data = []
    elif opcao == 'interest_by_region':
        pytrends.build_payload(palavras_chave, cat=0, timeframe='today 12-m', geo='', gprop='')
        data = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
        if not data.empty:
            data = data.reset_index().to_dict(orient='records')
        else:
            data = []
    elif opcao == 'related_queries':
        pytrends.build_payload(palavras_chave, cat=0, timeframe='today 12-m', geo='', gprop='')
        data = pytrends.related_queries()
    elif opcao == 'related_topics':
        pytrends.build_payload(palavras_chave, cat=0, timeframe='today 12-m', geo='', gprop='')
        data = pytrends.related_topics()
    else:
        return jsonify({"erro": "Opção inválida"}), 400

    return jsonify(data), 200

if __name__ == '__main__':
    app.run()
