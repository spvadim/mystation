import React, { useMemo, useState, useEffect, useRef } from "react";
import axios from 'axios';

import TableAddress from "../../components/Table/TableAddress.js";
import InputTextQr from "../../components/InputText/InputTextQr.js";
import Input from "../../components/InputText/Input.js";
import ModalWindow from "../../components/ModalWindow/index.js";

import { Notification_new } from "../../components/Notification_new";
import { Notification } from "../../components/Notification";

import { Button, Text, NotificationPanel, Switch} from "src/components";
import imgCross from 'src/assets/images/cross.svg';
import imgOk from 'src/assets/images/ok.svg';

import { Redirect } from "react-router-dom";

import address from "../../address.js";
import { createUseStyles } from "react-jss";
import { HeaderInfo } from './HeaderInfo';
import DataProvider from "src/components/DataProvider";

const getTableProps = (extended) => ({
    cube: {
        columns: extended ?
            [
                { name: "index", title: "№", width: 48 },
                { name: "created_at", title: "Создано", width: 123 },
                { name: "qr", title: "qr" },
                { name: "id", title: "id", width: 200 },
            ] : [
                { name: "index", title: "№", width: 48 },
                { name: "created_at", title: "Создано", width: 123 },
                { name: "qr", title: "qr" },
            ],
    },

    multipack: {
        columns: extended ?
            [
                { name: "index", title: "№", width: 48 },
                { name: "created_at", title: "Создано", width: 123 },
                { name: "qr", title: "qr", width: 48, Component: () => <>...</> },
                { name: "status", title: "Статус" },
                { name: "id", title: "id", width: 200 },
            ] : [
                { name: "index", title: "№", width: 48 },
                { name: "created_at", title: "Создано", width: 123 },
                { name: "qr", title: "qr" },
                { name: "status", title: "Статус" },
            ],
    },

    pack: {
        columns: extended ?
            [
                { name: "index", title: "№", width: 48 },
                { name: "created_at", title: "Создано", width: 123 },
                { name: "qr", title: "qr" },
                { name: "status", title: "Статус", width: 100 },
                { name: "id", title: "id", width: 200 },
            ] : [
                { name: "index", title: "№", width: 48 },
                { name: "created_at", title: "Создано", width: 123 },
                { name: "qr", title: "qr" },
                { name: "status", title: "Статус", width: 100 },
            ],
    },

});

const useStyles = createUseStyles({
    Main: {
        backgroundColor: ({ redBackground }) => redBackground && "#CC3333",
        display: 'flex',
        flexDirection: 'column',
        height: "100%",
    },
    header: {
        '& .button': {
            marginRight: 12,
        },
        display: 'flex',
        paddingLeft: 48,
        paddingRight: 48,
        paddingTop: 31,
        paddingBottom: 70,
    },
    headerInfo: {
        display: 'flex',
        flexGrow: 1,
        flexBasis: 0,
        justifyContent: 'space-between',
    },
    headerCenter: {
        display: 'flex',
        justifyContent: 'center',
        flexGrow: 1,
        flexBasis: 0,
    },
    headerRight: ({ mode }) => ({
        ...mode === 'auto' && { visibility: 'hidden' },
        display: 'flex',
        flexGrow: 1,
        flexBasis: 0,
    }),
    qrInput: {
        fontSize: 18,
        width: 177,
        marginLeft: 'auto',
    },
    tableContainer: {
        '& > div': {
            marginLeft: 12,
            flexBasis: 0,
            flexGrow: 1,
            height: 600,
        },
        flexGrow: 1,
        display: 'flex',
        paddingRight: 22,
        paddingLeft: 36,
    },
    tableTitle: {
        marginLeft: 12,
    },
    footer: {
        display: 'flex',
        position: "absolute",
        justifyContent: 'space-between',
        // paddingBottom: 22,
        paddingLeft: 27,
        paddingRight: 27,
        bottom: "1em",
        width: "calc(100% - 60px)"
        // marginTop: 50,
    },
    switchContainer: {
        userSelect: 'none',
        display: 'flex',
        alignItems: 'center',
        fontSize: 18,
    },
    selectContainer: {
        fontSize: 36,
        fontWeight: "bold"
    },
    switchTitle: {
        fontSize: 24,
        fontWeight: 700,
    },
    modalButtonIcon: {
        marginRight: 13,
    },
    notificationQrCodeImgContainer: {
        display: 'grid',
        columnGap: 9,
        gridAutoFlow: 'column',
        alignItems: 'center',
    },

    notificationPanel: {
        position: 'fixed',
        display: 'flex',
        flexWrap: 'wrap',
        gap: 10,
        maxHeight: "40%",
        overflowY: 'scroll',
        padding: 5,
        zIndex: 99,
        bottom: 90,
        left: 27,
        maxWidth: 260,
        backgroundColor: "#d4d4d4",
        borderRadius: 7,
    },


});

function Main() {
    const [mode, setMode] = useState('auto');
    const [redBackground, setRedBackground] = useState(false);
    const [batchSettings, setBatchSettings] = useState({});
    const [extended, setExtended] = useState(false);
    const [page, setPage] = useState('');

    const [modalDeletion, setModalDeletion] = useState(false);
    const [modalError, setModalError] = useState(false);
    const [modalCube, setModalCube] = useState(false);
    const [modalDisassemble, setModalDisassemble] = useState(false);
    const [modalDelete2Pallet, setModalDelete2Pallet]  = useState(false);
    const [modalPackingTableError, setModalPackingTableError] = useState(false);
    const [modalAgree, setModalAgree] = useState(false);
    const [modalChangePack, setModalChangePack] = useState(false);
    const [modalChangePackAgree, setModalChangePackAgree] = useState(false);
    const [modalWithdrawal, setModalWithdrawal] = useState(false);
    const [modalDesync, setModalDesync] = useState(false);

    const [events, setEvents] = useState([]);

    const [notificationText, setNotificationText] = useState("");
    const [notificationText2, setNotificationText2] = useState("");
    const [returnNotificationText, setReturnNotificationText] = useState("");
    const [notificationErrorText, setNotificationErrorText] = useState("");
    const [notificationPintsetErrorText, setNotificationPintsetErrorText] = useState("");
    const [notificationColumnErrorText, setNotificationColumnErrorText] = useState("");
    const [notificationDesyncErrorText, setNotificationDesyncErrorText] = useState("");
    const classes = useStyles({ mode, redBackground });
    const tableProps = useMemo(() => getTableProps(extended), [extended]);

    const [forceFocus, setForceFocus] = useState("inputQr");

    const inputQrRef = useRef();
    const inputQrCubeRef = useRef();
    const inputPackingTableRef = useRef();
    const inputDisassembleRef = useRef();
    const inputChangePackOldRef = useRef();
    const inputChangePackNewRef = useRef();

    const dictRefs = {
        inputQr: inputQrRef,
        inputQrCube: inputQrCubeRef,
        inputPackingTable: inputPackingTableRef,
        inputDisassemble: inputDisassembleRef,
        inputChangePackOld: inputChangePackOldRef,
        inputChangePackNew: inputChangePackNewRef,
    }

    const openHelp = () => {
        window.open("help").focus();
    }

    useEffect(() => {
        axios.get(address + "/api/v1_0/current_batch")
            .then(res => {
                setBatchSettings({
                    batchNumber: res.data.number.batch_number,
                    batchDate: res.data.number.batch_date.split("T")[0].split("-").reverse(), 
                    multipacks: res.data.params.multipacks,
                    packs: res.data.params.packs,
                    multipacksAfterPintset: res.data.params.multipacks_after_pintset,
                })
            })
            
        }, [setBatchSettings])

    useEffect(() => {
        axios.get(address + "/api/v1_0/settings")
            .then(res => {
                if (res.data.location_settings) {
                    document.title = "" + res.data.location_settings.place_name.value
                }
            })
    }, [])

    useEffect(() => {
        const request = () => {
            let request = axios.get(address + "/api/v1_0/events?processed=false&event_type=error")
            request.then(res => {
                setEvents(res.data.events);
            })

            axios.get(address + "/api/v1_0/get_mode")
            .then(res => {
                setMode(res.data.work_mode);
                if (res.data.work_mode === "auto") {
                    // setReturnNotificationText("");
                    setNotificationText2("");
                } else {
                    // setReturnNotificationText("Сосканируйте QR куба для редактирования");
                    setNotificationText2("Сосканируйте QR куба для редактирования");
                }
            })
            .catch(e => {
                // TOD0: handle error
                console.log(e);
            })
        }
        
        
        request();
        let timer = setInterval(() => {
            request();
        }, 1000);
        return () => clearInterval(timer);
    }, [])

    useEffect(() => {
        axios.get(address + "/api/v1_0/get_mode")
            .then(res => {
                setMode(res.data.work_mode);
                if (res.data.work_mode === "auto") setNotificationText2("")
                else {
                    // setReturnNotificationText2("Сосканируйте QR куба для редактирования");
                    setNotificationText2("Сосканируйте QR куба для редактирования");
                }
            })
            .catch(e => setNotificationErrorText(e.response.data.detail))
    }, [setMode]);

      useEffect(() => {
        const request = () => {
            let request = axios.get(address + "/api/v1_0/get_state");
            request.then(res => {
                let temp = res.data;
                if (temp.state === "normal") setNotificationColumnErrorText("")
                    else {setNotificationColumnErrorText(temp.error_msg)}  // setRedBackground(true)}
                if (temp.pintset_state === "normal") setNotificationPintsetErrorText("")
                    else {setNotificationPintsetErrorText(temp.pintset_error_msg)}  // setRedBackground(true)}
                if (temp.packing_table_state === "normal") setModalPackingTableError("")
                    else {setForceFocus("inputPackingTable"); setModalPackingTableError(temp.packing_table_error_msg)} // setRedBackground(true)}
                if (temp.pintset_withdrawal_state === "normal") setModalWithdrawal("")
                    else {setModalWithdrawal(temp.pintset_withdrawal_error_msg)} // setRedBackground(true)}
                if (temp.sync_state === "error") {setModalDesync(temp.sync_error_msg); setRedBackground(true)} //
                    else if (temp.sync_state === "fixing") {setNotificationDesyncErrorText("Рассинхрон")}    
                else {setModalDesync("")}

                // if (temp.state === "normal" && temp.pintset_state === "normal" && temp.packing_table_state === "normal" && temp.pintset_withdrawal_state === "normal" && temp.sync_state !== "error") setRedBackground(false);
                if (temp.sync_state !== "error") setRedBackground(false);
            })
            request.catch(e => setNotificationErrorText(e.response.data.detail))
        };
        request();
        const interval = setInterval(() => request(), 1000);
        return () => {clearInterval(interval)};
    }, []);

    useEffect (() => {
        let interval;
        let isExist = Object.keys(dictRefs).indexOf(forceFocus) !== -1;

        if (forceFocus && isExist) {
            interval = setInterval(() => {
                if (document.activeElement.id !== forceFocus && dictRefs[forceFocus].current
                    && !["INPUT", "SELECT"].includes(document.activeElement?.tagName ?? "")) {
                    dictRefs[forceFocus].current.focus();
                }
            }, 1000)
        } else if (!isExist) {
            interval = setInterval(() => {
                if (document.activeElement.id !== forceFocus) {
                    dictRefs["inputQr"].current.focus();
                }
            }, 1000);
        }       

        return () => {clearInterval(interval)};
    }, [forceFocus])

    if (page === "batch_params") {
        return (
            <Redirect to="/batch_params" />
        );
    } else if (page === "create") {
        return (
            <Redirect to="/create" />
        );
    } else if (page === "events") {
        return (
            <Redirect to="/events" />
        );
        // testing
    }else if(page === "main_new")
    {
        return(
            <Redirect to = "main_new"/>
        );
    }

    const returnNotification = () => {
        setNotificationText(returnNotificationText);
    }

    const updateMode = (newMode) => {
        axios.patch(address + "/api/v1_0/set_mode", { work_mode: newMode })
            .then(res => {
                setMode(res.data.work_mode);
                if (res.data.work_mode === "auto") {
                    // setReturnNotificationText("");
                    setNotificationText2("");
                } else if (res.data.work_mode === "manual") {
                    // setReturnNotificationText("Сосканируйте QR куба для редактирования");
                    setNotificationText2("Сосканируйте QR куба для редактирования");
                }
            })
            .catch(e => {
                // TOD0: handle error
                console.log(e);
            })
    }
  const createIncompleteCube = () => {
        axios.put(address + "/api/v1_0/cube_finish_manual/?qr=" + inputQrCubeRef.current.value.replace("/", "%2F"))
            .then(() => {
                setReturnNotificationText(notificationText);
                setNotificationText("Неполный куб успешно сформирован");
                setTimeout(() => {
                    returnNotification();
                }, 2000);
            })
            .catch(e => {
                setNotificationErrorText(e.response.data.detail)
            })
    }

    const closeProcessEvent = id => {
        axios.patch(address + "/api/v1_0/events/" + id)
    }

    return (
        <div className={classes.Main}>
            {modalDesync &&
                <ModalWindow
                    title="Оповещение о рассинхронизации"
                    description={modalDesync}
                >
                    <Button onClick={() => {
                        axios.patch(address + "/api/v1_0/set_sync_fixing")
                            .then(() => {
                                setNotificationDesyncErrorText("Рассинхрон");
                                setModalDesync(false);
                                // setRedBackground(false);
                            })
                    }}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Понял
                    </Button>
                </ModalWindow>
            }

            {modalWithdrawal && 
                <ModalWindow
                    title="Подтверждение выемки из-под пинцета"
                    description={modalWithdrawal}
                >
                    <Button onClick={() => {
                        axios.patch(address + "/api/v1_0/flush_pintset_withdrawal_with_remove")
                            .then(() => setModalWithdrawal(false))
                    }}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Вынимаю все
                    </Button>

                    <Button onClick={() => {
                        axios.patch(address + "/api/v1_0/flush_pintset_withdrawal")
                            .then(() => setModalWithdrawal(false))
                    }}>
                        Ничего не вынимаю
                    </Button>
                </ModalWindow>
            }

            {modalChangePackAgree && 
                <ModalWindow
                    title="Подтвердите действие"
                    description="Вы действительно хотите заменить пачку?"
                >
                    <Button onClick={modalChangePackAgree[0]}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Заменить
                    </Button>

                    <Button onClick={() => {setModalChangePackAgree(false); setForceFocus("inputQr")}}>
                        Отмена
                    </Button>
                </ModalWindow>
            }

            {modalChangePack && 
                <ModalWindow
                    title="Замена пачки"
                    description="На постах упаковки одну пачку можно заменить на другую. Для этого введите сначала QR старой пачки, потом QR новой пачки. Далее подтвердите свое действие"
                >
                    <Button onClick={() => {setModalChangePack(false); setForceFocus("inputQr")}}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Отмена
                    </Button>

                    <Input 
                        id="inputChangePackOld"
                        ref={inputChangePackOldRef}
                        onKeyPress={async e => {
                            if (e.charCode === 13) {
                                let req = axios.get(address + "/api/v1_0/packs/?qr=" + inputChangePackOldRef.current.value);
                                req.catch(e => {
                                    setNotificationErrorText(e.response.data.detail);
                                    inputChangePackOldRef.current.value = "";
                                    setTimeout(() => {
                                        setNotificationErrorText("");
                                    }, 2000);
                                })                                
                                let awaited = await req;
                                
                                if (awaited.data[0].id) {
                                    setForceFocus("inputChangePackNew");
                                }
                            }
                        }
                    }
                    />

                    <Input 
                        id="inputChangePackNew"
                        ref={inputChangePackNewRef}
                        onKeyPress={async e => {
                            if (e.charCode === 13) {
                                setModalChangePack(false);
                                let old = inputChangePackOldRef.current.value;
                                let new_ = inputChangePackNewRef.current.value;
                                let req = await (await axios.get(address + "/api/v1_0/packs/?qr=" + old)).data[0];

                                setModalChangePackAgree([() => {
                                    setForceFocus("inputQr");
                                    axios.patch(address + "/api/v1_0/packs/" + req.id, {"qr": new_, "to_process": false, "is_corrected": true})
                                        .then(() => {
                                            setModalChangePackAgree(false)
                                            axios.get(address + `/api/v1_0/packs/${req.id}/multipack_and_cube`)
                                            .then(ress => {
                                                let data = ress.data
                                                if (data.multipack_id)
                                                    axios.patch(address + `/api/v1_0/multipacks/${data.multipack_id}`, {"to_process": false, "is_corrected": true})                                        
                                                    .catch(e => setNotificationErrorText(e.response.data.detail))
                                                else
                                                    console.log(`Вызов /api/v1_0/packs/${req.id}/multipack_and_cube вернул пустой multipack_id`)

                                                if (data.cube_id)
                                                    axios.patch(address + `/api/v1_0/cubes/${data.cube_id}`, {"to_process": false, "is_corrected": true})                                        
                                                    .catch(e => setNotificationErrorText(e.response.data.detail))
                                                else
                                                    console.log(`Вызов /api/v1_0/packs/${req.id}/multipack_and_cube вернул пустой cube_id`)
                                            })
                                            .catch(() => console.log(`Вызов /api/v1_0/packs/${req.id}/multipack_and_cube не удался`))
                                        })
                                        .catch(e => setNotificationErrorText(e.response.data.detail))
                                }])
                                
                        }
                    }}
                    />

               </ModalWindow>
            }
            {modalAgree && 
                <ModalWindow
                    title="Подтвердите действие"
                    description="Вы действительно хотите удалить объект?"
                >
                    <Button onClick={() => {axios.delete((address + "/api/v1_0/cubes/" + modalAgree)).then(() => setModalAgree(false))}}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Удалить
                    </Button>

                    <Button onClick={() => {setModalAgree(false)}}>
                        Отмена
                    </Button>
                </ModalWindow>
            }

            {modalDisassemble && 
                <ModalWindow
                    title="Разобрать куб?"
                    description="Информация про куб и пачки в нем будет удалена из системы. Куб нужно будет распаковать, необходимые пачки нужно будет подкинуть перед камерой-счетчиком. Подтверждаете?"
                >
                    <Button onClick={() => {setModalDisassemble(false); setForceFocus("inputQr")}}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Отмена
                    </Button>

                    <Input  
                        id="inputDisassemble"
                        ref={inputDisassembleRef}
                        onKeyPress={async e => {
                            if (e.charCode === 13) {
                                let req = axios.get(address + "/api/v1_0/cubes/?qr=" + inputDisassembleRef.current.value);
                                req.catch(e => {
                                    setNotificationErrorText(e.response.data.detail);
                                    inputDisassembleRef.current.value = "";
                                    setTimeout(() => {
                                        setNotificationErrorText("");
                                    }, 2000);
                                })
                                let awaited = await req;

                                if (awaited.data.id) {
                                    setModalDisassemble(false);
                                    setModalAgree(awaited.data.id);
                                }
                            }
                        }}
                    />
               </ModalWindow>
            }

            {modalDelete2Pallet && 
                <ModalWindow
                    title="Удаление мультипаков"
                    description="Вы действительно хотите удалить мультипак(и)?"
                >
                    <Button onClick={() => {
                        axios.delete(address + "/api/v1_0/remove_multipacks_to_refresh_wrapper")
                        .then(() => setReturnNotificationText(notificationText), setNotificationText("Мультипаки успешно удалены"), setTimeout(returnNotification, 2000), setModalDelete2Pallet(false))
                            .catch(e => console.log(e.responce))
                    }}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Удалить
                    </Button>
                    <Button onClick={() => setModalDelete2Pallet(false)} theme="secondary">
                        <img className={classes.modalButtonIcon} src={imgCross} style={{ filter: 'invert(1)', width: 22 }} />
                        Отмена
                    </Button>
                </ModalWindow>
            }

            {modalPackingTableError  && 
                <ModalWindow
                    title="Ошибочный вывоз"
                    description={modalPackingTableError}
                >
                    <Button onClick={() => {
                        axios.patch(address + "/api/v1_0/flush_packing_table_with_remove")
                            .then(() => setModalPackingTableError(false), /*setValueQrModalPackingTable("")*/)
                            .catch(e => {
                                console.log(e.response);
                                setNotificationErrorText(e.response.data.detail)
                            })
                    }}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Удалить продукцию
                    </Button>
                    <Button onClick={() => {
                        axios.patch(address + "/api/v1_0/flush_packing_table")
                            .then(() => setModalPackingTableError(false), /*setValueQrModalPackingTable("")*/) // setRedBackground(false), )
                            .catch(e => setNotificationErrorText(e.responce.data.detail))
                    }}>
                        Отмена
                    </Button>
                    <Input
                        id="inputPackingTable"
                        ref={inputPackingTableRef}
                        placeholder="QR..."
                        onKeyPress={e => {
                            if (e.charCode === 13) {
                                axios.patch(address + "/api/v1_0/flush_packing_table_with_identify?qr=" + inputPackingTableRef.current.value)
                                    .then(() => {
                                        setModalPackingTableError(false);
                                        // setRedBackground(false);
                                        if (inputPackingTableRef.current) inputPackingTableRef.current.value = "";
                                        setReturnNotificationText(notificationText);
                                        setNotificationText("Успешно идентифицировано");
                                        setTimeout(returnNotification, 2000);
                                    })
                                    .catch(e => setNotificationErrorText(e.response.data.detail))
                            }
                        }}
                    />                </ModalWindow>
            }

            {modalDeletion && (
                <ModalWindow
                    title="Удаление объекта"
                    description="Информация про данную упаковку и составляющие будет удалена из системы. Пачку(и) нужно будет подкинуть перед камерой-счетчиком. Подтверждаете?"
                >
                    <Button onClick={() => {
                        setModalDeletion(false);
                        modalDeletion[0](modalDeletion[1])
                    }}>
                        <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                        Удалить
                    </Button>
                    <Button onClick={() => setModalDeletion(false)} theme="secondary">
                        <img className={classes.modalButtonIcon} src={imgCross} style={{ filter: 'invert(1)', width: 22 }} />
                        Отмена
                    </Button>
                </ModalWindow>
            )}
            {modalError && (
                <ModalWindow
                    title="Ошибка"
                    description={modalError !== true ? modalError.detail : "Вы используете QR вне куба. Пожалуйста перейдите в куб для редактирования."}
                >
                    <Button onClick={() => setModalError(false)}>Сбросить ошибку</Button>
                </ModalWindow>
            )}
            {modalCube && (
                <ModalWindow
                    title="Формирование неполного куба"
                    description="Из всех мультипаков и пачек в очереди будет сформирован куб. Подтверждаете?"
                >
                    <div style={{ display: "grid", gap: "2rem" }}>
                        <div>
                            <Input
                                id={"inputQrCube"}
                                ref={inputQrCubeRef}
                            />
                           
                        </div>
                        <div style={{ display: "flex", gap: "2rem" }}>
                            <Button onClick={() => {
                                if (inputQrCubeRef.current.value) {
                                    setForceFocus("inputQr");
                                    setModalCube(false);
                                    createIncompleteCube();
                                    inputQrCubeRef.current.value = "";
                                }
                            }}>
                                <img className={classes.modalButtonIcon} src={imgOk} style={{ width: 25 }} />
                                Создать
                            </Button>
                            <Button onClick={() => {
                                setForceFocus("inputQr");
                                setModalCube(false);
                                inputQrCubeRef.current.value = "";
                            }} theme="secondary">
                                <img className={classes.modalButtonIcon} src={imgCross} style={{ filter: 'invert(1)', width: 22 }} />
                                Отмена
                            </Button>
                        </div>
                    </div>
                </ModalWindow>
            )}

            <div className={classes.header}>
                <div className={classes.notificationPanel}>
                    { events.map(event => {
                        return <Notification_new
                            key={event.id}
                            text={event.message}
                            onClose={() => closeProcessEvent(event.id)}
                              />
                        })
                    }
                    {events.length > 1 ? <Button onClick={() => events.map(event => closeProcessEvent(event.id))}>Сбросить все ошибки</Button> : null}
                    <Button onClick={() => setPage("events")} >Перейти на страницу с ошибками</Button>
                </div>

                <div className={classes.headerInfo}>
                    <HeaderInfo title="Партия №:" amount={batchSettings.batchNumber} />
                    <HeaderInfo title="Дата" amount={batchSettings.batchDate ? batchSettings.batchDate.join(".") : null} />
                    <HeaderInfo title="Куб:" amount={batchSettings.multipacks} suffix="мультипака" />
                    <HeaderInfo title="Мультипак:" amount={batchSettings.packs} suffix="пачки" />
                    <HeaderInfo title="Пинцет:" amount={batchSettings.multipacksAfterPintset} suffix="мультипака" />
                </div>

                <div className={classes.headerCenter}>
                    <Button onClick={() => {setPage("batch_params")}} >Новая партия</Button>

                    <Button onClick={() => {
                        setModalDisassemble(true);
                        setForceFocus("inputDisassemble");
                    }}>Разобрать куб по его QR</Button>

                    <Button onClick={() => {setModalCube([createIncompleteCube]); setForceFocus("inputQrCube")}} >Сформировать неполный куб</Button>
                
                    {/*<Button onClick={() => {
                        setModalDelete2Pallet(true);
                        
                    }}>Удалить мультипак(и) для перезагрузки обмотчика</Button>*/}

                    <Button onClick={() => {setModalChangePack(true); setForceFocus("inputChangePackOld")}} >Заменить пачку на упаковке</Button>
                   
                </div>

                {/* <div className={classes.headerRight}> </div> */}
                <Button onClick={() => setPage("create")}>Новый куб</Button>
                <Button onClick={() => setPage("main_new")}>Новый интерфейс</Button>
                <InputTextQr
                    id="inputQr"
                    setNotification={setNotificationText}
                    setNotificationError={setNotificationErrorText}
                    mode={mode}
                    forceFocus={!modalCube && !modalPackingTableError}
                    hidden={!extended}
                    ref={inputQrRef}
                />
                <Button onClick={openHelp}>Справка</Button>
            </div>

            <div className={classes.tableContainer}>
                <div>
                    <Text className={classes.tableTitle} type="title2">Очередь кубов</Text>
                    <TableAddress
                        columns={tableProps.cube.columns}
                        setNotification={n => setNotificationText(n)}
                        notification={notificationText}
                        setError={(text) => setModalError(text)}
                        setModal={setModalDeletion}
                        type="cubes"
                        extended={extended}
                        address="/api/v1_0/cubes_queue"
                        buttonEdit="/edit"
                        buttonDelete="/trash"
                    />
                </div>

                <div>
                    <Text className={classes.tableTitle} type="title2">Очередь мультипаков</Text>
                    <TableAddress
                        columns={tableProps.multipack.columns}
                        setError={(text) => setModalError(text)}
                        setModal={setModalDeletion}
                        type="multipacks"
                        address="/api/v1_0/multipacks_queue"
                        buttonEdit="/edit"
                        buttonDelete="/trash"
                    />
                </div>

                <div>
                    <Text className={classes.tableTitle} type="title2">Очередь пачек</Text>
                    <TableAddress
                        columns={tableProps.pack.columns}
                        setError={(text) => setModalError(text)}
                        setModal={setModalDeletion}
                        type="packs"
                        address="/api/v1_0/packs_queue"
                        buttonDelete="/trash"
                    />
                </div>
            </div>

            <NotificationPanel
                style={{marginLeft: 276}}
                notifications={
                    [notificationText && (
                        <Notification
                            description={notificationText}
                        />
                    ),
                    notificationText2 && (
                        <Notification
                            description={notificationText2}
                        />
                    )]
                }
                errors={
                    [notificationErrorText && (
                        <Notification
                            error
                            description={notificationErrorText}
                        />
                    ),
                    notificationColumnErrorText && (
                        <Notification
                            error
                            description={notificationColumnErrorText}
                        />
                    ),
                    notificationDesyncErrorText && (
                        <Notification
                            error
                            description={notificationDesyncErrorText}
                        ><Button onClick={() => {
                            axios.patch(address + "/api/v1_0/flush_sync")
                                .then(() => {
                                    setNotificationDesyncErrorText("");
                                })
                        }}>Сбросить ошибку</Button></Notification>
                    ),
                    notificationPintsetErrorText && (
                        <Notification
                            error
                            description={notificationPintsetErrorText}
                        />
                    )]
                }
            />

            {/* 
            <ColumnError /> */}

            <div className={classes.footer}>
                <div style={{ display: "flex" }}>
                    <div>
                        <div className={classes.switchTitle}>
                            Режим управления:
                        </div>
                        <div className={classes.switchContainer}>
                            <select value={mode} onChange={e => updateMode(e.target.value)} className={classes.selectContainer} style={{color: (mode === "auto" ? "red" : (mode === "manual" ? "green" : "black"))}}>
                                <option value="auto" style={{color: "red"}}>Автоматический</option>
                                <option value="semi-auto" style={{color: "black"}}>Полуавтомат</option>
                                <option value="manual" style={{color: "green"}}>Ручной</option>
                            </select>
                        </div>
                    </div>

                    <div style={{display: "flex", gap: "321px"}}> 
                        {/* <NotificationPanel
                            errors={
                                [
                                    notificationPintsetErrorText && (
                                        <Notification
                                            title="Ошибка после пинцета"
                                            description={notificationPintsetErrorText}
                                            error
                                        > <Button onClick={() => flushPintsetError()}>Сбросить ошибку</Button>
                                        </Notification>
                                    ),
                                ]
                            }
                        />

                        <NotificationPanel
                            errors={
                                [
                                    notificationErrorText && (
                                        <Notification
                                            title="Ошибка"
                                            description={notificationErrorText}
                                            onClose={() => setNotificationErrorText("")}
                                            error
                                        />
                                    ),

                                    notificationColumnErrorText && (
                                        <Notification
                                            title="Ошибка колонны"
                                            description={notificationColumnErrorText}
                                            error
                                        > <Button onClick={() => flushStateColumn()}>Сбросить ошибку</Button>  </Notification>
                                    ),

                                    notificationDesyncErrorText && (
                                        <Notification
                                            title="Десинхронизация"
                                            description={notificationDesyncErrorText}
                                            error
                                        > <Button onClick={() => {
                                            axios.patch(address + "/api/v1_0/flush_sync")
                                                .then(() => {
                                                    setNotificationDesyncErrorText("");
                                                })
                                        }}>Сбросить ошибку</Button>  </Notification>
                                    )
                                ]
                            }
                        /> */}
                    </div>

                    

                </div>



                <div>
                    <div className={classes.switchTitle} style={{ textAlign: 'right' }}>
                        Вид интерфейса:
                    </div>
                    <div className={classes.switchContainer}>
                        Сжатый
                    <Switch onClick={() => setExtended(!extended)} />
                        Расширенный
                    </div>
                </div>

            </div>

        </div>
    );
}

export default Main;
