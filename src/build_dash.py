import json, pathlib, sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from dash_css import CSS
from dash_html import HTML
from model_js import MODEL_JS
R=pathlib.Path(__file__).resolve().parent.parent
bundle=(R/"data"/"bundle.json").read_text()
out=HTML.replace("__MODEL__",MODEL_JS).replace("__CSS__",CSS).replace("__BUNDLE__",bundle)
(R/"docs"/"index.html").write_text(out)
print(f"wrote docs/index.html  ({len(out)/1024:.0f} KB)")
