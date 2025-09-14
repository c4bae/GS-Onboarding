import { CommandResponse } from "../data/response"
import CommandRow from "./row"
import { deleteCommands } from "./command_api"

interface CommandTableProp {
  commands: CommandResponse[],
  setCommands: React.Dispatch<React.SetStateAction<CommandResponse[]>>
}

const CommandTable = ({
  commands,
  setCommands // props passed in
}: CommandTableProp) => {

  const handleDelete = (id: number) => {
    return async () => {
      const data = await deleteCommands(id)
      setCommands(data.data)
    }
  }

  return (
    <table>
      <thead>
        <tr>
          <th>ID: </th>
          <th>Main Command ID: </th>
          <th>Params: </th>
          <th>Status: </th>
          <th>Created On: </th>
          <th>Updated On: </th>
          <th>Delete</th>
        </tr>
      </thead>
      <thead>
        {commands.map(value => (<CommandRow key={value.id} {...value} handleDelete={handleDelete(value.id)} />))}
      </thead>
    </table>
  )
}

export default CommandTable;
