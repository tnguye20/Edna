import React, { FormEvent, useState } from 'react';
import { useAuthValue } from '../../contexts';
import { auth, db } from '../../libraries';
import {
  TextField,
  Button,
  Collapse
} from '@material-ui/core';
import Alert from '@material-ui/lab/Alert';

import { useAlert } from '../../hooks/';

import * as ALERT_TYPES from '../../constants/alerts';

export const SignupForm = () => {
  const { setAuthUser } = useAuthValue();
  const [ email, setEmail ] = useState("");
  const [ password, setPassword ] = useState("");
  const [ displayName, setDisplayName ] = useState("");
  const { alertOpen, alertType, alertMsg, setAlertOpen, setAlertMsg, setAlertType } = useAlert();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const { user } = await auth.createUserWithEmailAndPassword(email, password);
      if (user) {
        const { uid } = user;
        await db.collection("users").doc(uid).set({
          displayName,
          email,
        });
        setAlertMsg(ALERT_TYPES.ALERT_SUCCESS_SIGNUP_MSG);
        setAlertType(ALERT_TYPES.ALERT_SUCCESS);
        setAlertOpen(true);
        setTimeout( () => { setAuthUser(user) }, 3000);
      }
    } catch (err) {
      const { message } = err;
      if ( message !== undefined ){
        setAlertMsg(message);
      } else {
        setAlertMsg(ALERT_TYPES.ALERT_DEFAULT_MSG);
      }
      setAlertType(ALERT_TYPES.ALERT_ERROR);
      setAlertOpen(true);
    }
  }

  return (
    <>
      <Collapse in={alertOpen}>
        <Alert
          severity={alertType}
          onClose={() => setAlertOpen(false)}
        >
          { alertMsg }
        </Alert>
        <br />
      </Collapse>

      <form noValidate autoComplete="off" method="POST" action="/signup" onSubmit={handleSubmit}>
        <TextField
          autoFocus
          id="email"
          color="secondary"
          label="Email"
          fullWidth
          onChange={e => setEmail(e.target.value)}
        />
        <br /><br /><br />
        <TextField
          id="name"
          color="secondary"
          label="Display Name"
          fullWidth
          onChange={e => setDisplayName(e.target.value)}
        />
        <br /><br /><br />
        <TextField
          id="password"
          type="password"
          color="secondary"
          label="Password"
          fullWidth
          onChange={e => setPassword(e.target.value)}
        />
        <br /><br /><br />
        <Button variant="contained" color="secondary" fullWidth type="submit">
          Sign Up
        </Button>
      </form>
    </>
  )
}
