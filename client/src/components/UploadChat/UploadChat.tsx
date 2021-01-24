import * as React from 'react';
import { auth, storage } from '../../libraries';
import { useAuthValue } from '../../contexts';
import { useAlert } from '../../hooks';
import { edna } from '../../api';

import {
  Grid,
  Container,
  Typography,
  Button,
  Collapse
} from '@material-ui/core';
import Alert from '@material-ui/lab/Alert';
import './index.css';

import { ALERT_TYPES } from '../../constants/';

export const UploadChat: React.FunctionComponent = () => {
    const { authUser } = useAuthValue();
    const fullStoragePath = `${authUser.uid}/WhatsApp/`;

    const uploadInputRef = React.useRef<HTMLInputElement>(null);
    const file = React.useRef<File>();

    const [canUpload, setCanUpload] = React.useState(false);
    const { alertOpen, alertType, alertMsg, setAlertOpen, setAlertMsg, setAlertType } = useAlert();

    const handleOnChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        let files = e.target.files;
        setAlertOpen(false);
        try { 
            if (files && files.length === 1) {
                if (files[0].type !== 'application/zip') {
                    throw new Error(ALERT_TYPES.ALERT_ERROR_UPLOAD_TYPE);
                }
                file.current = files[0];
                console.log(file.current)
                setCanUpload(true);
            }
            else {
                throw new Error('No File To Upload.')
            }
        }
        catch (error) {
           setAlertType(ALERT_TYPES.ALERT_ERROR);
           setAlertMsg(error.message);
           setAlertOpen(true);
        }
    }

    const handleOnClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault();
        if(uploadInputRef.current) {
            uploadInputRef.current.click();
        }
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (file.current) {
            const currentFile = file.current;
            const uploadTask = storage.child(`${fullStoragePath}${currentFile.name}`).put(currentFile);
            uploadTask.on('state_change', function(snapshot) {

            },
            function (error) {
                file.current = undefined;
                setCanUpload(false);
            }, async function (){
                /**
                 * Call Cloud Run to execute data conversion
                 */
                try {
                    await edna.init(authUser.idToken, currentFile.name);
                    await edna.generate(authUser.idToken);
                }
                catch (error) {
                    setAlertType(ALERT_TYPES.ALERT_ERROR);
                    setAlertMsg(error.message);
                    setAlertOpen(true);
                }
                finally {
                    file.current = undefined;
                    setCanUpload(false);
                }
            });
        }
    };

    return (
        <>
            <Container maxWidth="sm">
            <Grid
                container
                spacing={0}
                direction="column"
                justify="center"
                style={{ minHeight: '100vh'}}
            >
                <Grid item xs={12} sm={12}>
                    <Typography
                    align="center"
                    variant="h2"
                    component="h3"
                    gutterBottom
                    >
                    Upload Chat History
                    </Typography>

                    <Collapse in={alertOpen}>
                        <Alert
                        severity={alertType}
                        onClose={() => setAlertOpen(false)}
                        >
                        { alertMsg }
                        </Alert>
                        <br />
                    </Collapse>

                    <form onSubmit={handleSubmit}>
                        <input type='file' name='chat_upload' id='chat_upload' onChange={handleOnChange} ref={uploadInputRef}/>
                        <Grid
                            container
                            justify="space-around"
                            alignItems="center"
                            spacing={5}
                            direction="column"
                        >
                            <Grid item xs={12} sm={6}>
                                <Button variant='contained' color='secondary' centerRipple onClick={handleOnClick}>
                                    Load File
                                </Button>
                            </Grid>
                            {
                                canUpload
                                ? (
                                    <Grid item xs={12} sm={6}>
                                        <Button type='submit' variant='contained' color='primary' centerRipple>
                                            Upload
                                        </Button>
                                    </Grid>
                                ) : ''
                            }
                        </Grid>
                    </form>
                </Grid>
            </Grid>
            </Container>
        </>
    );
}
