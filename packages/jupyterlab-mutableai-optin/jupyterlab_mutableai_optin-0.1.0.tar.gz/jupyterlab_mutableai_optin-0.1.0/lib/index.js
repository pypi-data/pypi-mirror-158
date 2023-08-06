import { showDialog } from "@jupyterlab/apputils";
import { IMutableAI } from "jupyterlab_mutableai";
import parse from "html-react-parser";
import mutable from "../style/images/mutable.png";

const SHOWN_OPTIN = "jupyterlab_mutableai_optin:shown";

export default [
  {
    id: 'jupyterlab_mutableai_optin',
    requires: [IMutableAI],
    autoStart: true,
    activate: function (app, mutableManager) {
      console.log(
        'JupyterLab extension jupyterlab_mutableai_optin is activated!'
      );

      let { localStorage } = window;

      function showOptIn() {
        let p = showDialog({
          body: parse(`<div style="max-width: 500px;">
          <div style="text-align: center;"><img style="width: 100%; max-width: 300px; padding-bottom: 2em;" src="${mutable}" /></div>
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
];
