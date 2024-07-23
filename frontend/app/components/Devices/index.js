'use client'
import { useState, useEffect } from 'react'  

const API_URL = 'http://localhost:8000'

export const Devices = () => {
	const [devices, setDevices] = useState([])

	useEffect(() => {
		const main = async () => {
			const res = await (await fetch(API_URL)).json()
			console.log(res)
			setDevices(res)
		}
		main()
	}, [])

	return (
		<ul className='max-w-[400px] w-[100%] m-auto bg-neutral-900 grid gap-1'>
		{
			devices.map((val) => {
				return (
					<li key={val[0]} className='bg-neutral-800 text-white p-4'>
						<div className='header grid grid-cols-2'>

							<h1 className='col-span-1'>{val[3]}</h1>
					
							<div className='col-span-1 text-sm text-end text-neutral-500'>{
								val[4] == 1 ? <span className='text-lime-400'>On-line</span> : val[5].slice(0, 19) 
							}</div>

							<h2 className='text-sm text-neutral-500'>{val[1]}</h2>
							<h3 className='text-sm text-neutral-500 text-end'>{val[6]}</h3>

						</div>
					</li>
				)
			})
		}
		</ul>
	)
}
