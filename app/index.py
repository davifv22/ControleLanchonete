from app import *

bp = Blueprint('index', __name__)


@bp.route('/',methods=['POST', 'GET'])
def index_():
    return render_template('index/index.html')