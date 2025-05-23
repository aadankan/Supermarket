const AdminPanel = (props: {adminPanel: () => void}) => {
  return (
    <div className="h-40 w-full p-6 flex justify-end items-center">
        <div
          className="h-16 px-7 py-4 bg-amber-500 rounded-3xl shadow-[0px_0px_6.5px_1.62px_rgba(232,158,0,0.50)] shadow-[3.25px_3.25px_6.51px_0px_rgba(0,0,0,0.25)] inline-flex justify-center items-center gap-4 overflow-hidden cursor-pointer"
          onClick={props.adminPanel}
        >
          <div className="justify-start text-white text-2xl font-normal [text-shadow:_7px_7px_7px_rgb(0_0_0_/_0.25)]">
            Admin panel
          </div>
        </div>
      </div>
  )
}

export default AdminPanel