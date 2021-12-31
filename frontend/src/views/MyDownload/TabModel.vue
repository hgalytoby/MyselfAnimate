<template>
  <button type="button" class="btn btn-success" @click="clearFinishDownload">清除已完成</button>
  <button type="button" class="btn btn-danger" data-bs-toggle="modal" :data-bs-target="`#${props.target}`">
    刪除動漫
  </button>
  <div class="modal fade" :id="props.target" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">刪除動漫</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          確定要刪除勾選的動漫?
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="deleteAnimate" data-bs-dismiss="modal">確認</button>
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { sendSocketMessage } from '../../hooks/useWS'

export default {
  name: 'TabModel',
  props: {
    target: String,
    clearAction: String
  },
  setup (props) {
    const clearFinishDownload = () => {
      sendSocketMessage({
        action: props.clearAction
      })
    }
    function deleteAnimate () {

    }
    return {
      clearFinishDownload,
      deleteAnimate,
      props
    }
  }
}
</script>

<style scoped>

</style>
