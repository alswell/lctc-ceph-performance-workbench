/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Form, Icon, Input, Button, Modal, Row, Col, Select } from 'antd'
const { TextArea } = Input;
import PropTypes from 'prop-types'
import './TestForm.less'
import { fetchAndNotification } from '../../services/restfulService'
const FormItem = Form.Item

function hasErrors (fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field])
}

class TestTestForm extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      spinning: true,
      data: null,
      id: window.location.pathname ? window.location.pathname.substr(window.location.pathname.lastIndexOf("/") + 1)
        : ""
    }
  }

  componentDidMount () {
    // To disabled submit button at the beginning.
    this.props.form.validateFields()
  }

  handleSubmit = (e) => {
    e.preventDefault()
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values)

        this.props.onCancel()
        fetchAndNotification({
          //url: `initimage/${this.state.id}`,
          url: `initimage/${this.state.id}/`,
          method: 'post',
          params: values,
          notifications: {
            title: 'Init Image Action',
            success: `创建${values.clustername} 操作成功！`,
            error: `创建${values.clustername} 操作失败！`,
          },
        }).then((result)=>{
          //when the fetch successfully ,refresh the table
          this.props.refresh()
        })
      }
    })
  };

  handleChange = (value) => {
      console.log(`selected ${value}`);
    };


  render () {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched, getFieldValue } = this.props.form

    // Only show error after a field is touched.
    const userNameError = isFieldTouched('userName') && getFieldError('userName')
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 6 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 14 },
      },
    };
    const formItemLayoutWithOutLabel = {
      wrapperCol: {
        xs: { span: 24, offset: 0 },
        sm: { span: 11, offset: 6 },
      },
    };

    return (
      <Modal
        visible={this.props.visible}
        title="Init Images"
        onCancel={this.props.onCancel}
        width={1000}
        footer={null}
      >
        <Form onSubmit={this.handleSubmit}>
          <FormItem
            {...formItemLayout}
            label="Image Name"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('imagename', {
              rules: [
                { required: true, message: 'Please input the image name!' },
              ],
            })(
              <Input placeholder="testimage" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Image Size"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('imagesize', {
              initialValue: "1024M",
              rules: [
                { required: true, message: 'Please input the image size!' },
              ],
            })(
              <Select style={{ width: 120 }} onChange={this.handleChange}>
                <Option value="1024">1024M</Option>
                <Option value="102400">102400M</Option>
              </Select>
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Image Number"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('imagenum', {
              rules: [
                { required: true, message: 'Please input the image number!' },
              ],
            })(
              <Input placeholder="6" />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label="Pool"
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('pool', {
              initialValue: "rbd",
              rules: [
                { required: true, message: 'Please input the pool!' },
              ],
            })(
              <Input placeholder="rbd" />
            )}
          </FormItem>
          <FormItem>
            <Button
              type="primary"
              htmlType="submit"
              disabled={hasErrors(getFieldsError())}
            >
              Create
            </Button>
          </FormItem>
        </Form>
      </Modal>
    )
  }
}

TestTestForm.propTypes = {
  form: PropTypes.object,
  onCancel: PropTypes.function,
  visible: PropTypes.boolean,
}

const TestForm = Form.create()(TestTestForm)

export default TestForm
