from app import app
from app.models import Results
from flask import jsonify

#@app.route('/api/results/<int:id>', methods=['GET'])
#def get_results(id):
#   data = Results.query.get_or_404(id).to_dict()
#   return jsonify(data)

@app.route('/api/results', methods=['GET'])
def get_results():
   data = Results.query.all()
   
   list = [ 
        {
        'id': self.id,
        'text': self.text,
        'date': self.date.isoformat() + 'Z',
        'p1_teamA': self.p1_teamA,
        'p2_teamA': self.p2_teamA,
        'p1_teamB': self.p1_teamB,
        'p2_teamB': self.p2_teamB,
        'points_teamA': self.points_teamA,
        'points_teamB': self.points_teamB,
        } for self in data
   ]
   return jsonify(list)
