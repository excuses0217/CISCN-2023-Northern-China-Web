from scanner.core.base_scan import BaseScan
from copy import deepcopy


class HtmlXssScan(BaseScan):
    attack_vectors = ['<script>alert(1)</script>',
                      '<img src=1 onerror=alert(1)',
                      '<iframe src="javascript:alert(1)">']


class JsXssScan(BaseScan):
    attack_vectors = ['window.location=javascript:alert(1)//',
                      'eval("alert(1)")//',
                      ';alert(1);//']


