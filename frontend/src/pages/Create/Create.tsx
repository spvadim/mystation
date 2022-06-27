import React, { createRef, useEffect, useReducer, useState } from 'react';
import axios from "axios";
import { Redirect } from "react-router-dom";

import TableData from "../../components/Table/TableData.js";
import address from "../../address.js";
import ModalWindow from "../../components/ModalWindow/index.js";
import { Text, InputRadio, Button } from 'src/components';
import imgCross from 'src/assets/images/cross.svg';
import imgOk from 'src/assets/images/ok.svg';

import "./Create.scss"
import NotificationProvider from 'src/components/NotificationProvider';
import DataProvider from 'src/components/DataProvider';
import { ProductionBatchParams } from 'src/interfaces/ProductionBatchParams.js';
import { ProductionBatchInput } from 'src/interfaces/ProductionBatchInput.js';

const CtxCurrentMultipack = React.createContext({
    currentMultipack: null,
    setCurrentMultipack: () => console.warn,
});

const RadioCurrentMultipack = ({ index }) => {
    const { currentMultipack, setCurrentMultipack } = React.useContext(CtxCurrentMultipack);
    return (
        <InputRadio name="multipacksChoose"
            htmlFor={index}
            key={index}
            checked={index === currentMultipack}
            onChange={() => setCurrentMultipack(index)}
            className="radio-multipack">
            {index + 1}
        </InputRadio>
    )
}

const tableProps = {
    multipacksTable: {
        name: "multipacksTable",
        columns: [
            {
                name: "radioButton",
                title: "№",
                Component: RadioCurrentMultipack,
            },
        ],
        buttonDelete: "/delete",
    },
    packsTable: {
        name: "packsTable",
        columns: [
            { name: "number", title: "№", width: 64 },
            { name: "qr", title: "QR", width: 'auto' },
        ],
        buttonDelete: "/delete",
    }

};

const RedirectBack = () => {
    let params = new URLSearchParams(window.location.search);
    window.location.href = params.get("origin") ?? "/"
}

const Create = () => {
    const [page, setPage] = useState('');
    const [batchIndex, setBatchIndex] = useState<number>();
    const [params, setParams] = useState<ProductionBatchParams[]>([]);
    const [settings, setSettings] = useState<ProductionBatchParams>();
    const [cubeQr, setCubeQr] = useState('');
    const [packQr, setPackQr] = useState('');
    const [modalCancel, setModalCancel] = useState(false);
    const [modalSubmit, setModalSubmit] = useState(false);
    const [modalAddNewBatch, setModalAddNewBatch] = useState(false);
    const [barcode, setBarcode] = useState('');
    const [multipacksTableData, setMultipacksTableData] = useState<{to_process: boolean, packs: {qr: string, to_process: boolean}[]}[]>([]);
    const [currentMultipack, setCurrentMultipack] = useState<number>(-1);

    const refBatch = createRef<HTMLSelectElement>();
    const refCubeQR = createRef<HTMLInputElement>();
    const refPackBar = createRef<HTMLInputElement>();
    const refPacksQR = createRef<HTMLInputElement>();

    const setFocus = (ref: React.RefObject<HTMLInputElement | HTMLSelectElement>) => ref.current?.focus();
    const [, forceUpdate] = useReducer(x => x + 1, 0);

    const loadBatches = () => {
        DataProvider.Batches.load()
        .then(res => {
            DataProvider.Batches.data = res.data.filter(x => x.params.visible).reverse().slice(0, 10);
            forceUpdate();
        })
    }

    useEffect(loadBatches, [])
    
    useEffect(() => {
        axios.get(address + "/api/v1_0/settings")
            .then(res => {
                if (res.data.location_settings) {
                    document.title = "Новый куб: " + res.data.location_settings.place_name.value
                }
            })
    }, [])

    useEffect(() => {
        axios.get<ProductionBatchParams[]>(address + "/api/v1_0/batches_params")
            .then(res => setParams(res.data))
            .catch(e => console.log(e.response))
    }, [])

    useEffect(() => {
        axios.get(address + "/api/v1_0/settings")
            .then(res => {
                if (res.data.location_settings) {
                    document.title = "Новый куб: " + res.data.location_settings.place_name.value
                }
            })
    }, [])

    const deletePack = (indexPack: number, indexMultipack: number) => {
        let temp = multipacksTableData.slice();
        temp[indexMultipack].packs.splice(indexPack, 1);
        temp[indexMultipack].to_process = temp[indexMultipack].packs.some(x => x.to_process);
        setMultipacksTableData(temp);
    }

    const deleteMultipack = (index: number) => {
        if (index === -1) return false;
        let temp = multipacksTableData.slice();
        temp.splice(index, 1);
        setMultipacksTableData(temp);
    }

    const checkExist = () => {
        let errorText = "";
        if (!settings || !settings.id) errorText = "Параметры партии не заданы!"
        else if (batchIndex === undefined) errorText = "Партия не выбрана!"
        else if (!cubeQr) errorText = "QR куба не задан!"
        else if (!barcode) errorText = "Штрихкод не задан!"
        else if (multipacksTableData.length === 0) errorText = "Очередь мультипаков пуста!"

        if (errorText !== "") NotificationProvider.createError(errorText)
        return errorText === "";
    }

    const submitChanges = () => {
        if (!checkExist()) return false;
        if (!settings || batchIndex === undefined || DataProvider.Batches.data === undefined) return false;

        let body = {
            params_id: settings.id,
            batch_number: DataProvider.Batches.data[batchIndex].number.batch_number,
            qr: cubeQr,
            barcode_for_packs: barcode,
            content: multipacksTableData.map(x => x.packs.map(x => {return {"qr": x.qr}})),
        }

        axios.put(address + "/api/v1_0/cube_with_new_content", body)
            .then(res => 
                axios.patch(address + `/api/v1_0/cubes/${res.data.id}`, {"is_corrected": true}).then(RedirectBack))
            .catch(e => {
                NotificationProvider.createError(e.response.data.detail ? e.response.data.detail : e.message)
                if (e.response.data.detail) {
                    let text: string = e.response.data.detail;
                    let qr = text.substr("Пачка с QR-кодом ".length, text.length - "Пачка с QR-кодом  уже есть в системе".length);
                    let temp = multipacksTableData.slice();
                    let found = false;
                    for (let i = 0; i < temp.length; i++) {
                        for (let j = 0; j < temp[i].packs.length; j++) {
                            if ( temp[i].packs[j].qr == qr) {
                                found = true;
                                temp[i].packs[j].to_process = true;
                                break;
                            }
                        }
                        if (found) temp[i].to_process = true;
                        if (found) break;
                    }
                    setMultipacksTableData(temp);
                }
            })
    }

    const closeChanges = () => {
        setModalCancel([setPage, "/"]);
        RedirectBack();
    }

    const checkLocalQrUnique = (qr: string): boolean => {
        let finded = multipacksTableData.find(arr => {
            return arr.packs.find(pack => pack.qr === qr)
        })

        return finded ? false : true
    }

    const checkGlobalQrUnique = (qr: string): Promise<boolean> => {
        return axios.get<{unique: boolean}>(address + `/api/v1_0/packs/unique/?qr=${qr}`)
        .then(e => e.data.unique)
        .catch(() => {
            NotificationProvider.createError("Ошибка проверки уникальности")
            //Потом изменить
            return true;
        });
    }

    const addEmptyMultipack = () => {
        if (!settings) return;
        if (multipacksTableData.length >= settings.multipacks) {
            NotificationProvider.createError("Превышен предел мульпаков");
            return false;
        }

        let temp = multipacksTableData.slice();
        temp.push({to_process: false, packs: []});
        setMultipacksTableData(temp);
        return temp;
    }

    const addPackToMultipack = async (qr: string, indexMultipack_: number) => {
        if (!settings || !settings.id) {
            NotificationProvider.createError("Сначала выберите параметры партии!");
            setPackQr("");
            return false;
        }

        if (!qr) return false;
        if (!checkLocalQrUnique(qr)) return false;
        
        let unique = await checkGlobalQrUnique(qr);
        let indexMultipack = indexMultipack_;
        let temp = multipacksTableData.slice();
        let packs = temp[indexMultipack];

        if (!packs) {
            addEmptyMultipack();
            setCurrentMultipack(0);
            packs = {to_process: false, packs: []};
            indexMultipack = 0;
        }

        if (packs.packs.length >= settings.packs) {
            if (!addEmptyMultipack()) return false;
            setCurrentMultipack(multipacksTableData.length);
            packs = {to_process: false, packs: []};
            packs.packs.push({ qr, to_process: !unique });
            packs.to_process = packs.packs.some(x => x.to_process);
            temp[multipacksTableData.length] = packs;

            setMultipacksTableData(temp);
        } else {
            packs.packs.push({ qr, to_process: !unique });
            packs.to_process = packs.packs.some(x => x.to_process);
            temp[indexMultipack] = packs;

            setMultipacksTableData(temp);
        }

        setPackQr("");
    }

    if (page === "/") return <Redirect to="/" />

    const applyFocus = () => setTimeout(() => {
        if (window.screen.width < 640) return;
        if (["INPUT", "SELECT"].includes(document.activeElement?.tagName ?? "")) return;

        let ref: React.RefObject<HTMLInputElement | HTMLSelectElement> = refBatch;
        if (batchIndex !== undefined) ref = refCubeQR;
        if (cubeQr !== "") ref = refPackBar;
        if (barcode !== "") ref = refPacksQR;
        setFocus(ref)
    }, 1000)

    const confirmButtons = (mobile: boolean) => {
        return (
            <div style={{display: "grid", placeItems: "center"}}>
                <div className={"button-container " + (mobile ? "desktop-hidden" : "mobile-hidden")}>
                    <Button onClick={() => setModalSubmit([submitChanges])} className="button-submit">
                        <img src={imgOk} /><span>Принять изменения</span>
                    </Button>
                    <Button onClick={() => setModalCancel([closeChanges])} theme="secondary">
                        <img src={imgCross} style={{ filter: 'invert(1)' }} /><span>Отменить изменения</span>
                    </Button>
                </div>
            </div>
        )
    }

    const selectBatch = (value: string) => {
        if (value === "new") {
            setModalAddNewBatch(true);
            if (refBatch.current)
                refBatch.current.selectedIndex = 0;
        }
        else setBatchIndex(+value);
    }

    return (
        <div className="edit" style={{padding: "10px 15px"}}>
            {ModalNewBatch(modalAddNewBatch, setModalAddNewBatch)}
            {modalCancel && (
                <ModalWindow
                    title="Отменить изменения"
                    description="Вы действительно хотите отменить изменения?"
                >
                    <Button onClick={() => {
                        modalCancel[0](modalCancel[1]);
                        setModalCancel(false);
                    }}>
                        <img className="modal-button-icon" src={imgOk} style={{ width: 25 }} />
                        Отменить
                    </Button>
                    <Button onClick={() => setModalCancel(false)} theme="secondary">
                        <img className="modal-button-icon" src={imgCross} style={{ filter: 'invert(1)', width: 22 }} />
                        Вернуться к изменениям
                    </Button>
                </ModalWindow>
            )}
            {modalSubmit && (
                <ModalWindow
                    title="Принять изменения"
                    description="Вы действительно хотите принять изменения?"
                >
                    <Button onClick={() => {
                        modalSubmit[0](modalSubmit[1]);
                        setModalSubmit(false);
                    }}>
                        <img className="modal-button-icon" src={imgOk} style={{ width: 25 }} />
                        Принять изменения
                    </Button>
                    <Button onClick={() => setModalSubmit(false)} theme="secondary">
                        <img className="modal-button-icon" src={imgCross} style={{ filter: 'invert(1)', width: 22 }} />
                        Отменить
                    </Button>
                </ModalWindow>
            )}
            <div className="inline-table header">
                <Text type="title" style={{marginRight: "64px"}}>Создание</Text>
                <div className="input-table">
                    <div className="input-container">
                        <span className="title2">Партия ГП:</span>
                        {DataProvider.Batches.data !== undefined && (
                            <select autoFocus onChange={e => selectBatch(e.target.value)}
                            ref={refBatch} onBlur={applyFocus}>
                                <option hidden disabled selected>Выберите партию</option>
                                {/*<option value="new">Добавить новую партию</option>*/}
                                {DataProvider.Batches.data.map((x, i) => <option value={i} key={i}>
                                        Номер: {x.number.batch_number} Дата: {x.number.batch_date}
                                    </option>)}
                            </select>
                        )}
                    </div>
                        
                    <div className="input-container">
                        <span className="title2">QR куба: </span>
                        <input
                            placeholder="0000"
                            name="cube_qr"
                            type="text"
                            onBlur={applyFocus}
                            ref={refCubeQR}
                            value={cubeQr}
                            onChange={e => setCubeQr(e.target.value)}
                        />
                    </div>

                    <div className="input-container">
                        <span className="title2">Штрихкод каждой пачки в кубе: </span>
                        <input
                            placeholder="0000"
                            name="barcode"
                            type="text"
                            ref={refPackBar}
                            value={barcode}
                            onChange={e => setBarcode(e.target.value)}
                            onBlur={applyFocus}
                        />
                    </div>
                </div>

                {confirmButtons(false)}
            </div>

            <div className="inline-table">
                <div className="form">
                    <Text className="table-title" type="title2">Параметры партии</Text>
                    {params.filter(x => x.visible).map((obj, index) => (
                        <InputRadio name="param_batch"
                            htmlFor={obj.id}
                            key={index}
                            onClick={() => setSettings(obj)}>
                            <span className="radio-label">
                                Куб: {obj.multipacks} мультипаков, мультипак: {obj.packs} пачек,
                                    <br />
                                    пинцет: {obj.multipacks_after_pintset} мультипаков
                            </span>
                        </InputRadio>
                    ))}
                </div>

                <div>
                    <div className="table-title-container" style={{justifyContent: "space-between", alignItems: "center"}}>
                        <Text className="table-title" type="title2">Мультипаки</Text>
                        <Button style={{margin: "0 auto"}} className="button" onClick={() => addEmptyMultipack()}>Добавить</Button>
                    </div>
                    <CtxCurrentMultipack.Provider value={{ currentMultipack, setCurrentMultipack }}>
                        <TableData
                            rows={multipacksTableData}
                            className="table-content"
                            onDelete={obj => {
                                deleteMultipack(multipacksTableData.indexOf(obj))
                            }}
                            hideTracksWhenNotNeeded
                            {...tableProps.multipacksTable}
                        />
                    </CtxCurrentMultipack.Provider>
                </div>

                <div>
                    <div className="table-title-container" style={{justifyContent: "space-between", alignItems: "center"}}>
                        <Text className="table-title" type="title2">Пачки</Text>
                        <input style={{fontSize: "1.25rem"}}
                            placeholder="0000"
                            name="pack_qr"
                            type="text"
                            value={packQr}
                            ref={refPacksQR}
                            onBlur={applyFocus}
                            onChange={e => setPackQr(e.target.value)}
                            onKeyPress={e => (e.charCode === 13) && addPackToMultipack(packQr, currentMultipack)}
                        />
                    </div>
                    <TableData
                        rows={multipacksTableData[currentMultipack] ?
                            multipacksTableData[currentMultipack].packs.map((obj, index) => ({ number: index + 1, qr: obj.qr, to_process: obj.to_process })) :
                            []}
                        className="table-content"
                        onDelete={obj => deletePack(obj.number - 1, currentMultipack)}
                        hideTracksWhenNotNeeded
                        {...tableProps.packsTable}
                    />
                </div>
            </div>
                {confirmButtons(true)}
        </div>
    );
}

export default Create;

//0:40
const ModalNewBatch = (visible: boolean, setModalVisible: (visible: boolean)=>any) => {
    const [date, setDate] = useState<string>();
    const [number, setNumber] = useState<number>();

    const cancel = () => setModalVisible(false);
    const handle = () => {
        if (number === undefined || date === undefined) return;
        let data: ProductionBatchInput = {
            number: {batch_number: number, batch_date: date},
            params_id: "dasdas"
        }
        axios.put<ProductionBatchInput>(address + `/api/v1_0/batches`, data);
    }

    return (
        <>
            {visible && <ModalWindow title="Добавление новой партии" description>
                <div className="setting-inner">
                    <div className="row">
                        <span className="cell1">Номер партии:</span>
                        <input className="input" value={number} onChange={e => setNumber(+e.target.value)}/>
                    </div>
                    <div className="row">
                        <span className="cell1">Дата создания партии:</span>
                        <input className="input" value={date} placeholder="2021-01-20 00:00" onChange={e => setDate(e.target.value)}/>
                    </div>
                    <div className="flex-between-center">
                        <Button onClick={handle}>
                            <img className="modal-button-icon" alt="✔" src={imgOk} />Добавить</Button>
                        <Button onClick={cancel}>Отмена</Button>
                    </div>
                </div>
            </ModalWindow>}
        </>
    )
}