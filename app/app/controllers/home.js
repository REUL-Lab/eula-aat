import config from '../config/environment';
import Controller from '@ember/controller';
import { inject as service } from '@ember/service';

/* eslint-disable no-unused-vars */
export default Controller.extend({
  ajax: service(),
  urlToFetch: null,
  init: function () {
    this._super();
    this.set('fileName', null);
  },
  actions: {
    chooseFile() {
      $('.file-upload-input').click()
    },
    updateFilename() {
      const file = $('.file-upload-input').get(0).files[0];
      this.set('fileName', file.name);
    },
    uploadFile() {
      const formData = new FormData();

      const file = $('.file-upload-input').get(0).files[0];
      formData.append('contents', file );

      const extension = file.name.split('.').get('lastObject');
      formData.append('doctype', extension);

      const request = this.get('ajax').post(`http://${config.APP.apiDomain}/api/eula/upload`, {
        processData: false,
        contentType: false,
        data: formData
      });

      try {
        request.then((idOfReport) => {
          if (typeof idOfReport === 'string') {
            this.transitionToRoute(`/analysis/${idOfReport}`);
          } else {
            this.transitionToRoute('/');
            alert('Invalid file submitted.');
          }
        }, (failure) => {
          this.transitionToRoute('/');
          alert('There was an error processing your request.');
        });
      } catch (e) {
        this.transitionToRoute('/');
        alert('There was an error processing your request.');
      }
    },
    fetchData() {
      this.transitionToRoute('processing.eula');
      const requestData = { url: this.get('urlToFetch') };
      const request = this.get('ajax').post(`http://${config.APP.apiDomain}/api/eula/fetch`, { data: requestData });
      try {
        request.then((idOfReport) => {
          if (typeof idOfReport === 'string') {
            this.transitionToRoute(`/analysis/${idOfReport}`);
          } else {
            this.transitionToRoute('/');
            alert('Invalid URL submitted.');
          }
        }, (failure) => {
          this.transitionToRoute('/');
          alert('There was an error processing your request.');
        });
      } catch (e) {
        this.transitionToRoute('/');
        alert('There was an error processing your request.');
      }
    }
  }
});