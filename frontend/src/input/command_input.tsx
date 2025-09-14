import { useState, useEffect } from "react";
import { CommandResponse, MainCommandResponse } from "../data/response"
import { getMainCommands } from "./input_api";
import { API_URL } from "../environment";
import { CommandRequest } from "../data/request";
import "./command_input.css"
import axios from "axios";


interface CommandInputProp {
  setCommands: React.Dispatch<React.SetStateAction<CommandResponse[]>>
}

const CommandInput = ({ setCommands }: CommandInputProp) => {
  const [selectedCommand, setSelectedCommand] = useState<MainCommandResponse | null>(null);
  const [parameters, setParameters] = useState<{ [key: string]: string }>({});
  const [mainCommands, setMainCommands] = useState<MainCommandResponse[] | null>(null);

  useEffect(() => {
      getMainCommands().then(data => {
        setMainCommands(data.data)
    })
  }, [])

  const handleParameterChange = (param: string, value: string): void => {
    setParameters((prev) => ({
      ...prev,
      [param]: value,
    }));
  }

  const handleSubmit = async (e: React.FormEvent) => {
    if(!selectedCommand) {
      return
    }

    try {
      const command: CommandRequest = {
        command_type: selectedCommand.id,
        params: selectedCommand.params,
    };
      await axios.post(`${API_URL}/commands/`, command);
      console.log('Command created successfully');
    }
    catch(e) {
      console.error(e)
      throw e
    }

    // returns a response object, so destructure to get the desired data
    const { data } = await axios.get<CommandResponse>(`${API_URL}/commands/`)
    // setCommands accepts CommandResponse[]
    setCommands(commands => [...commands, data])
  }

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedCommand(mainCommands?.find((command) => command.name === e.target.value) || null); 
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="spreader">
          <div>
            <label>Command Type: </label>
            <select onChange={handleChange}>
                {!mainCommands ? <option>Loading commands...</option> : mainCommands.map((command: MainCommandResponse) => {
                  return <option key={command.id}>{command.name}</option>
                })}

            </select>
          </div>
          {selectedCommand?.params?.split(",").map((param) => (
            <div key={param}>
              <label htmlFor={`param-${param}`}>{param}: </label>
              <input
                id={`param-${param}`}
                type="text"
                value={parameters[param] || ""}
                onChange={(e) => handleParameterChange(param, e.target.value)}
                placeholder={`Enter ${param}`}
              />
            </div>
          ))}
          <button type="submit">Submit</button>
        </div>
      </form>
    </>
  )
}

export default CommandInput;
