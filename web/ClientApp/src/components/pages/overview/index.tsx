import * as React from 'react';
import Layout from '../../layout/main/Layout';
import { RouteComponentProps } from 'react-router-dom';
import RackSlot from '../../ui/rackSlot'
import ElevatorControler from '../../ui/elevatorController'

import SockerMessages from '../../ui/socketMessages'

export default class Overview extends React.Component<RouteComponentProps<any>, {}> {
    public render() {
        const slots = [];
        for (let slot = 0; slot < 5; slot++) {
            slots.push( <RackSlot key={slot} slotNo={slot+1}></RackSlot> )
        }

        return <Layout showHeaderFooter={true}>
        <div className="grid">
            <h1>Robo Desk</h1>
            <div className="grid__row">
                <div className="grid__col grid__col--1">
                    <div className="teaser">
                        <div className="teaser__txt">
                            <div className="teaser__body">
                                {slots}
                            </div>
                        </div>
                    </div>
                </div>

                <div className="grid__col grid__col--2">
                    <div className="teaser">
                        <div className="teaser__body">
                            <ElevatorControler></ElevatorControler>
                            <SockerMessages/>
                        </div>
                    </div>
                </div>

            </div>
        </div>
        </Layout>;
    }
}
