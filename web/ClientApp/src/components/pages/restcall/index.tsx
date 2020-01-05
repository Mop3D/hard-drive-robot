import * as React from 'react';
import axios from 'axios';
import { has } from 'lodash';
import Layout from '../../layout/main/Layout';
import Loading from '../../ui/loading';
import MessageBox from '../../ui/messageBox';

interface IOwnProps {
}

interface IOwnState {
    loading: boolean;
    hasError: boolean;
    returnData: any;
}

//
// class: Manage Admins
// 
export default class ManageAdmins extends React.Component<IOwnProps, IOwnState | {}> {

    // state
    state = {
        loading: true,
        hasError: false,
        returnData: null
    }

    // component did mount
    componentDidMount() {
        document.title = "REST call";
        this.getAllRecords();
    }

    //  Validate Response Object, by checking it's structure.
    isGetAllRecordsResultValid = (responseData: any) => {
        return responseData.data !== null && has(responseData.data, 'key');
    }
    //
    // get the Department data
    //
    getAllRecords = async () => {
        const APIENDPOINT = `${process.env.PUBLIC_URL}/files/testData.json`;

        /* get dropdown data */
        const res = await axios.get(APIENDPOINT);
        const { data } = await res;
        try {
            console.log("getAllRecords", data)

            if (this.isGetAllRecordsResultValid(data)) {
                //  Store response data into components state.
                this.setState({
                    returnData: data,
                    loading: false,
                    hasError: false
                });
            } else {
                console.error("getAllRecords - no valid data", data);
                this.setState({ loading: false, hasError: true });
            }
        } catch (e) {
            console.error("getAllRecords - error data", e);
            this.setState({ loading: false, hasError: true });
        }
    }
    //*********************************************
    //render
    //
    render() {
        const { hasError, loading, returnData } = this.state;

        let pageContent = <div />;
        if (loading) {
            pageContent = <Loading />;
        } else if (hasError) {
            pageContent = <MessageBox msg="An error occured. Please try again later!" className="error" />;
        } else {
            pageContent = <p>
                <textarea defaultValue={returnData ? JSON.stringify(returnData) : ""} cols={40} rows={10} />
                </p>
        }

        return (
            <Layout showHeaderFooter={true}>
                {/* content */}
                {pageContent}
            </Layout>
        )
    }
}