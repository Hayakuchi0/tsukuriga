import { ready, ajaxForm } from '../utils'

ready(() => {
  ajaxForm("#direct-message-form",()=>{
    if(location.href.match('/u/')&&location.href.match('/direct_messages')) {
      location.reload(true);
    }
  });
});
