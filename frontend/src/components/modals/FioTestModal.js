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
//import Container from "../../routes/chart/lineChart/index"



class FioTestModal extends React.Component {
  // constructor (props) {
  //   super(props)
  // }

  componentDidMount () {

  }

    render () {

      const Container = ({ children, ratio = 5 / 2, minHeight = 250, maxHeight = 350 }) => <div className={styles.container} style={{ minHeight, maxHeight }}>
        <div style={{ marginTop: `${100 / ratio}%` || '100%' }}></div>
        <div className={styles.content} style={{ minHeight, maxHeight }}>
          <ResponsiveContainer>
            {children}
          </ResponsiveContainer>
        </div>
      </div>

      const SimpleLineChart = ({data}) => {
        return (
          <Container>
            <LineChart data={data} margin={{
              top: 5,
              right: 30,
              left: 20,
              bottom: 5,
            }}>
              <XAxis dataKey="id" />
              <YAxis />
              <CartesianGrid strokeDasharray="3 3" />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="iops" stroke="#8884d8"/>
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
          closable={false}
        >
          <SimpleLineChart data={this.props.selectedItems}/>
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
}

export default FioTestModal
