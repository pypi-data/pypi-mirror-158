"use strict";
(self["webpackChunkjupyterlab_mutableai_optin"] = self["webpackChunkjupyterlab_mutableai_optin"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var jupyterlab_mutableai__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jupyterlab_mutableai */ "webpack/sharing/consume/default/jupyterlab_mutableai");
/* harmony import */ var jupyterlab_mutableai__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jupyterlab_mutableai__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var html_react_parser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! html-react-parser */ "webpack/sharing/consume/default/html-react-parser/html-react-parser");
/* harmony import */ var html_react_parser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(html_react_parser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _style_images_mutable_png__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/images/mutable.png */ "./style/images/mutable.png");





const SHOWN_OPTIN = "jupyterlab_mutableai_optin:shown";

/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([
  {
    id: 'jupyterlab_mutableai_optin',
    requires: [jupyterlab_mutableai__WEBPACK_IMPORTED_MODULE_1__.IMutableAI],
    autoStart: true,
    activate: function (app, mutableManager) {
      console.log(
        'JupyterLab extension jupyterlab_mutableai_optin is activated!'
      );

      let { localStorage } = window;

      function showOptIn() {
        let p = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
          body: html_react_parser__WEBPACK_IMPORTED_MODULE_2___default()(`<div style="max-width: 500px;">
          <div style="text-align: center;"><img style="width: 100%; max-width: 300px; padding-bottom: 2em;" src="${_style_images_mutable_png__WEBPACK_IMPORTED_MODULE_3__["default"]}" /></div>
          Enable Mutable AI in JupyterLab to get AI powered code intelligence features:<br>
          <br>
          <div style="padding-left: 1em">✅ Transform to production quality code</div>
          <br>
          <div style="padding-left: 1em">✨ Automatic type annotations</div>
          <br>
          <div style="padding-left: 1em">📖 AI based documentation generation</div>
          <br>
          <span style='font-size: 0.9em;'>If enabled, code you transform is sent to, but not stored on, Mutable AI and their third party servers. Learn more on the <a style="text-decoration: underline;" href="https://mutableai.com">MutableAI website</a>.</span></div>
          `),
        })
        p.then((r) => {
          if (r.button.accept) {
            mutableManager.enable();
          } else {
            mutableManager.disable();
          }
          localStorage.setItem(SHOWN_OPTIN, true);
        });
      }

      function initOptin() {
        // No callback for readiness unfortunately
        let readyInterval = setInterval(() => {
          if (app.shell.isAttached) {
            showOptIn()
            clearInterval(readyInterval);
          }
        }, 10);
      }

      if (!localStorage.getItem(SHOWN_OPTIN)) {
        // Disable by default
        mutableManager.disable();

        // Then ask to enable
        initOptin();
      }
    }
  }
]);


/***/ }),

/***/ "./style/images/mutable.png":
/*!**********************************!*\
  !*** ./style/images/mutable.png ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (__webpack_require__.p + "551302024f9f9dcad3fd02d7bbfcd628cf81d75a81202edb87758d23aaa619ab.png");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.15c7afe06aa7d42f9bf8.js.map