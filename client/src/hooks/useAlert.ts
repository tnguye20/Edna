import { useState } from 'react';

import * as ALERT_TYPES from '../constants/alerts';

export const useAlert = () => {
  const [ alertOpen, setAlertOpen ] = useState(false);
  const [ alertType, setAlertType ] = useState(ALERT_TYPES.ALERT_SUCCESS);
  const [ alertMsg, setAlertMsg ] = useState(ALERT_TYPES.ALERT_SUCCESS_MSG);

  return {
    alertMsg,
    alertOpen,
    alertType,
    setAlertMsg,
    setAlertType,
    setAlertOpen
  }
}