/*
	opyright (C) 2007-2017 Claude SIMON (http://q37.info/contact/).
	This file is part of RNCq.

	RNCq is free software: you can redistribute it and/or
	modify it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	RNCq is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
	Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with RNCq. If not, see <http://www.gnu.org/licenses/>.
*/

// Once installed ('npm install rncq'), launch 'npm explore rncq -- node test.js'.

const rncq = require('./RNCq.js');
var expr = "784512.8456120*8456120.48651320-84651320.896451320/84651230.89645120*86451320.7984651230/84651320.789465120";

console.log( rncq.componentInfo() ) ;
console.log(rncq.wrapperInfo());

const arg = process.argv[2];

if (arg != undefined)
    expr = arg;

process.stdout.write(rncq.returnArgument("Text from JS file") + '\n');

rncq.evaluate( expr, (result) => process.stdout.write(result));
