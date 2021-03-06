/**
 * Created by chenkang1 on 2017/7/2.
 */
import React from 'react'
import { Modal } from 'antd'
import PropTypes from 'prop-types'
import {
  Button,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import styles from './Container.less'
import {fetchAndNotification} from "../../services/restfulService";
//import Container from "../../routes/chart/lineChart/index"



class FioTestModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      data: {},
    }
  }

  componentDidMount() {
    this.fetchDetail()
  }

  fetchDetail = () => {
    const caseids = this.props.selectedRowKeys

    fetchAndNotification({
      url: `fiotest`,
      method: 'get',
      params: {'id': caseids},
      notifications:{
        error: `获取数据失败！`,
      }
    }).then((result) => {
      this.setState({
        spinning: false,
        data: result.data
      })
    })
  }

    render () {
      console.log(this.state.data)

      const Container = ({ children, ratio = 5 / 2, minHeight = 250, maxHeight = 350 }) => <div className={styles.container} style={{ minHeight, maxHeight }}>
        <div style={{ marginTop: `${100 / ratio}%` || '100%' }}></div>
        <div className={styles.content} style={{ minHeight, maxHeight }}>
          <ResponsiveContainer>
            {children}
          </ResponsiveContainer>
        </div>
      </div>

      const SimpleLineChart = ({data, type}) => {
        //console.log(data)
        return (
          <Container>
            <LineChart data={data} margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}>
              <XAxis dataKey="short_name" />
              <YAxis />
              <CartesianGrid strokeDasharray="3 3" />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey={type} stroke="#8884d8"/>
            </LineChart>
          </Container>
        )
      }


    return (
      <div>
        <Modal
          title={this.props.title}
          visible={this.props.visible}
          onOk={this.props.onOk}
          onCancel={this.props.onCancel}
          width={1000}
          footer={null}
        >
          <SimpleLineChart data={this.state.data.data} type={this.props.type}/>
        </Modal>
      </div>
    )
  }

}


FioTestModal.propTypes = {
  title: PropTypes.string,
  visible: PropTypes.boolean,
  onOk: PropTypes.function,
  onCancel: PropTypes.function,
  selectedItems: PropTypes.array,
  selectedRowKeys: PropTypes.array,
  type: PropTypes.string,
}

export default FioTestModal
