import * as React from 'react';
import Layout from '../../layout/main/Layout';
import { RouteComponentProps } from 'react-router-dom';

export default class Overview extends React.Component<RouteComponentProps<any>, {}> {
    public render() {      
        return <Layout showHeaderFooter={true}>
            <div className="PlayGround">
            <p>1. Example: Custom font</p>
            <h1>Hello, test custom font!</h1>
            <br />
            <p>2. Example: Background image in .scss file</p>
            <div className="bg-img">
                This div has a background image
            </div>
            <br />
            <p>3. Example: Png Image as img HTML tag.</p>
            <img src="dist/styles/images/portrait.jpg" />
            <br />
            <p>4. Example: Bootstrap variable overwrite. Overwrites must be done in _custom_bootstrap.scss file</p>
            <button type="button" className="btn btn-primary">Primary</button>
            <br />
            <p>5. Example: Simple Bootstrap grid</p>
            <div className="row">
                <div className="col-sm-4">.col-sm-4</div>
                <div className="col-sm-4">.col-sm-4</div>
                <div className="col-sm-4">.col-sm-4</div>
            </div>
            <br />
            <p>6. Example: SVG as background image in .scss</p>
            <div className="svg-bg-img">
                
            </div>
            <br />
            <p>6. Example: SVG as img HTML tag</p>
            <img src="dist/styles/images/logo-siemens-ingenuity-for-life-dark.svg" />
        </div>
        </Layout>;
    }
}
