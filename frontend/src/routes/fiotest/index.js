/**
 * Created by chenkang1 on 2017/6/30.
 */
import React from "react";
import PropTypes from "prop-types";
import { connect } from "dva";
import DataTable from "../../components/BasicTable/DataTable";
import { Modal, Row, Col, Card, Button, Table } from "antd";
import { Link } from "dva/router";
import DropOption from "../../components/DropOption/DropOption";
import FioTestModal from "../../components/modals/FioTestModal";
import { fetchAndNotification } from "../../services/restfulService";
import { parse } from 'qs'

const confirm = Modal.confirm;

class FioTest extends React.Component {
  // constructor (props) {
  //   super(props)
  // }

  componentDidMount() {
    //console.log("did");
  }

  componentWillMount() {
    // let param = parse(window.location.search,{
    //     ignoreQueryPrefix:true
    //   })
    // this.props.host.jobid = param.jobid
  }

  handleMenuClick = (record, e) => {
    if (e.key === "1") {
      confirm({
        title: "Are you sure delete this record?",
        onOk() {
          console.log(record);
          confirm({
        title: "Are you sure delete this record?",
        onOk() {
          console.log(record);
        }
      });
        }
      });
    } else if (e.key === "2") {
      confirm({
        title: "Are you sure delete this record?",
        onOk() {
          console.log(record);
        }
      });
    }
  };

  showModal = key => {
    let { dispatch } = this.props;
    dispatch({
      type: "fiotest/showModal",
      payload: {
        key
      }
    });
  };

  refresh = () => {
    this.props.dispatch({ type: "fiotest/refresh" });
  };

  init = () => {
    this.tableDataProps = {
      columns: [
        {
          title: "Job ID",
          dataIndex: "jobid",
          key: "jobid",
          sorter: true
        },
        {
          title: "Case Name",
          dataIndex: "short_name",
          key: "short_name",
          //width: 350,
          sorter: true
        },
        {
          title: "Status",
          dataIndex: "status",
          key: "status",
          sorter: true
        },
        // {
        //   title: 'Block Size',
        //   dataIndex: 'blocksize',
        //   key: 'blocksize',
        //   sorter: true,
        // }, {
        //   title: 'IO Depth',
        //   dataIndex: 'iodepth',
        //   key: 'iodepth',
        //   sorter: true,
        // }, {
        //   title: 'Number Job',
        //   dataIndex: 'numberjob',
        //   key: 'numberjob',
        //   sorter: true,
        // },
        // {
        //   title: 'Image Number',
        //   dataIndex: 'imagenum',
        //   key: 'imagenum',
        // }, {
        //   title: 'clientnum',
        //   dataIndex: 'clientnum',
        //   key: 'clientnum',
        // }, {
        //   title: 'readwrite',
        //   dataIndex: 'readwrite',
        //   key: 'readwrite',
        // },
        {
          title: "Read IOPS",
          dataIndex: "r_iops",
          key: "r_iops"
        },
        {
          title: "Write IOPS",
          dataIndex: "w_iops",
          key: "w_iops"
        },
        {
          title: "IOPS",
          dataIndex: "iops",
          key: "iops"
        },
        {
          title: "Read BW(MiB/s)",
          dataIndex: "r_bw",
          key: "r_bw"
        },
        {
          title: "Write BW(MiB/s)",
          dataIndex: "w_bw",
          key: "w_bw"
        },
        {
          title: "BW(MiB/s)",
          dataIndex: "bw",
          key: "bw"
        },
        {
          title: "LAT(ms)",
          dataIndex: "lat",
          key: "lat"
        },
        {
          title: "Sys data",
          //dataIndex: 'sysdata',
          //key: 'sysdate',
          render: (text, record) =>
            <Link to={`sysdata?caseid=${record.id}`}>sys data</Link>
        },
        {
          title: "Perf dump",
          //dataIndex: 'sysdata',
          //key: 'sysdate',
          render: (text, record) =>
            <Link to={`perfdump/${record.id}`}>perf dump</Link>
        },
        {
          title: "Full Case Name",
          dataIndex: "case_name",
          key: "case_name",
          width: 350,
          sorter: true
        }
      ],
      fetchData: {
        url: this.props.host.jobid
          ? `fiotest/${this.props.host.jobid}/`
          : `fiotest`,
        params: null
      },
      errorMsg: "get fiotest table error",
      refresh: this.props.host.refresh,
      handleSelectItems: (selectedRowKeys, selectedRows) => {
        this.props.dispatch({
          type: "fiotest/updateSelectItems",
          payload: [selectedRowKeys, selectedRows]
        });
      }
    };

    this.iopsModalProps = {
      visible: this.props.host.iopsModalVisible,
      maskClosable: true,
      title: "",
      type: "iops",
      wrapClassName: "vertical-center-modal",
      selectedItems: this.props.host.selectedItems,
      selectedRowKeys: this.props.host.selectedRowKeys,
      onCancel: () => {
        let { dispatch } = this.props;
        dispatch({
          type: "fiotest/hideModal",
          payload: {
            key: "iopsModalVisible"
          }
        });
      }
    };

    this.latModalProps = {
      visible: this.props.host.latModalVisible,
      maskClosable: true,
      title: "",
      type: "lat",
      wrapClassName: "vertical-center-modal",
      selectedItems: this.props.host.selectedItems,
      selectedRowKeys: this.props.host.selectedRowKeys,
      onCancel: () => {
        let { dispatch } = this.props;
        dispatch({
          type: "fiotest/hideModal",
          payload: {
            key: "latModalVisible"
          }
        });
      }
    };

    this.bwModalProps = {
      visible: this.props.host.bwModalVisible,
      maskClosable: true,
      title: "",
      type: "bw",
      wrapClassName: "vertical-center-modal",
      selectedItems: this.props.host.selectedItems,
      selectedRowKeys: this.props.host.selectedRowKeys,
      onCancel: () => {
        let { dispatch } = this.props;
        dispatch({
          type: "fiotest/hideModal",
          payload: {
            key: "bwModalVisible"
          }
        });
      }
    };
  };

  render() {
    this.init();
    return (
      <div className="content-inner">
        <Row gutter={32}>
          <Col lg={24} md={24}>
            <Card>
              <div className="action-btn-container">
                <Button type="primary" onClick={this.refresh} icon="reload" />
                <Button
                  type="primary"
                  onClick={this.showModal.bind(this, "iopsModalVisible")}
                  disabled={this.props.host.selectedItems.length === 0}
                >
                  IOPS Chart
                </Button>
                <Button
                  type="primary"
                  onClick={this.showModal.bind(this, "latModalVisible")}
                  disabled={this.props.host.selectedItems.length === 0}
                >
                  Lat Chart
                </Button>
                <Button
                  type="primary"
                  onClick={this.showModal.bind(this, "bwModalVisible")}
                  disabled={this.props.host.selectedItems.length === 0}
                >
                  BW Chart
                </Button>
              </div>
              <DataTable {...this.tableDataProps} scroll={{ x: 1600 }} />
            </Card>
          </Col>
        </Row>
        {this.props.host.iopsModalVisible &&
          <FioTestModal {...this.iopsModalProps} />}
        {this.props.host.latModalVisible &&
          <FioTestModal {...this.latModalProps} />}
        {this.props.host.bwModalVisible &&
          <FioTestModal {...this.bwModalProps} />}
      </div>
    );
  }
}

function mapStateToProps({ fiotest }) {
  return {
    host: fiotest
  };
}

FioTest.propTypes = {
  cluster: PropTypes.object,
  location: PropTypes.object,
  dispatch: PropTypes.func,
  loading: PropTypes.object,
  host: PropTypes.object
};

export default connect(mapStateToProps)(FioTest);
