/**
 * Created by chenkang1 on 2017/7/4.
 */
import React from 'react'
import { Form, Icon, Input, Button, Modal } from 'antd'
import PropTypes from 'prop-types'
import { fetchAndNotification } from '../../services/restfulService'
const FormItem = Form.Item

function hasErrors (fieldsError) {
  return Object.keys(fieldsError).some(field => fieldsError[field])
}

class NormalLoginForm extends React.Component {

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
          url: 'create',
          method: 'post',
          params: values,
          notifications: {
            title: 'create Action',
            success: `创建${values.userName} 操作成功！`,
            error: `创建${values.userName} 操作失败！`,
          },
        })
      }
    })
  };

  render () {
    const { getFieldDecorator, getFieldsError, getFieldError, isFieldTouched } = this.props.form

    // Only show error after a field is touched.
    const userNameError = isFieldTouched('userName') && getFieldError('userName')
    const passwordError = isFieldTouched('password') && getFieldError('password')
    const emailError = isFieldTouched('email') && getFieldError('email')

    return (
      <Modal
        visible={this.props.visible}
        title="Create a new job"
        okText="Create"
        footer={null}
        onCancel={this.props.onCancel}
        // onOk={this.onCreate}
      >
        <Form layout="vertical" onSubmit={this.handleSubmit}>
          <FormItem
            validateStatus={userNameError ? 'error' : ''}
            help={userNameError || ''}
          >
            {getFieldDecorator('JobName', {
              rules: [
                { required: true, message: 'Please input your jobname!' },
              ],
            })(
              <Input placeholder="Jobname" />
            )}
          </FormItem>
          <FormItem
            validateStatus={passwordError ? 'error' : ''}
            help={passwordError || ''}
          >
            {getFieldDecorator('BlockSize', {
              rules: [{ required: true, message: 'Please select the blockszie!' }],
            })(
              <Input type="password" placeholder="Password" />
            )}
          </FormItem>
          <FormItem
            validateStatus={emailError ? 'error' : ''}
            help={emailError || ''}
          >
            {getFieldDecorator('email', {
              rules: [
                { required: true, message: 'Please input your Password!' },
                { type: 'email', message: 'The input is not valid E-mail!' },
              ],
            })(
              <Input type="text" placeholder="Email" />
            )}
          </FormItem>
          <FormItem>
            <Button
              type="primary"
              htmlType="submit"
              disabled={hasErrors(getFieldsError())}
            >
              Log in
            </Button>
          </FormItem>
        </Form>
      </Modal>
    )
  }
}

NormalLoginForm.propTypes = {
  form: PropTypes.object,
  onCancel: PropTypes.function,
  visible: PropTypes.boolean,
}

const CollectionCreateForm = Form.create()(NormalLoginForm)

export default CollectionCreateForm
