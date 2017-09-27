/*
	Copyright (C) 2007-2017 Claude SIMON (http://q37.info/contact/).

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

# include "rncqnjs.h"

#include "registry.h"

#include "rncalg.h"
#include "rncrpn.h"

#include "sclmisc.h"
#include "sclnjs.h"

void sclnjs::SCLNJSInfo( txf::sOFlow &Flow )
{
	Flow << NAME_MC << " v" << VERSION << txf::nl
		 << txf::pad << "Build : " __DATE__ " " __TIME__ " (" << cpe::GetDescription() << ')';
}

namespace {
	SCLNJS_F( ReturnArgument_ )
	{
	qRH
		str::wString Input, Text;
	qRB
		Input.Init();
		Caller.GetArgument( Input );

		Text.Init();
		sclmisc::GetBaseTranslation( "Argument", Text, Input );

		Caller.SetReturnValue( Text );
		qRR
		qRT
		qRE
	}

	namespace {
		namespace {
			struct rRack_ {
			public:
				str::wString Expression, Result;
				qRMV( sclnjs::rCallback, C, Callback );
				bso::sBool RPN;	// if 'true' 'Expression' is RPN ('ab+'), otherwise is algebraic ('a+b').
				void reset( bso::sBool P = true )
				{
					if ( P ) {
						if ( Callback != NULL )
							delete Callback;
					}

					tol::reset( P, Callback, Expression );
				}
				qCDTOR( rRack_ );
				void Init( bso::sBool RPN )
				{
					Expression.Init();
					Result.Init();
					Callback = NULL;
					this->RPN = RPN;
				}
			};

			bso::sBool Evaluate_(
				xtf::sIFlow &XFlow,
				bso::sBool RPN,
				txf::sOFlow &OFlow )
			{
				bso::sBool Success = false;
			qRH
				mthrtn::wRational Number;
			qRB
				Number.Init();

			if ( RPN )
				Success = rncrpn::Evaluate<mthrtn::dRational, mthrtn::wRational, rncrtn::dRationals, rncrtn::wRationals>( XFlow, Number );
			else
				Success = rncalg::Evaluate<mthrtn::dRational, mthrtn::wRational, rncrtn::dRationals, rncrtn::wRationals>( XFlow, Number );

				if ( Success ) {
					Number.Simplify();

					OFlow << Number.N << " / " << Number.D;
				}
			qRR
			qRT
			qRE
				return Success;
			}

			bso::sBool Evaluate_(
				xtf::sIFlow &XFlow,
				bso::sBool RPN,
				str::dString &Result )
			{
				bso::sBool Success = false;
			qRH
				flx::rStringTOflow OFlow;
			qRB
				OFlow.Init( Result );

				Success = Evaluate_( XFlow, RPN, OFlow );
			qRR
			qRT
			qRE
				return Success;
			}

			bso::sBool Evaluate_( 
				str::dString &Expression,
				bso::sBool RPN,
				str::dString &Result )
			{
				bso::sBool Success = false;
			qRH
				flx::sStringIFlow IFlow;
				xtf::sIFlow XFlow;
			qRB
				IFlow.Init( Expression );
				XFlow.Init( IFlow, utf::f_Guess );

				Success = Evaluate_( XFlow, RPN, Result );
			qRR
			qRT
			qRE
				return Success;
			}

			typedef sclnjs::cAsync cAsync_;

			class rRackAsyncCallback_
			: public rRack_,
 			  public cAsync_
			{
			protected:
				void SCLNJSWork( void ) override
				{
					if ( !Evaluate_( Expression, RPN, Result ) )
						sclmisc::GetBaseTranslation( "BadExpression", Result );
				}
				sclnjs::eBehavior SCLNJSAfter( void ) override
				{
					C().Launch( Result );

					return sclnjs::bExitAndDelete;
				}
			public:
				void reset( bso::sBool P = true )
				{
					rRack_::reset( P );
				}
				qCVDTOR( rRackAsyncCallback_ );
			};

			void Evaluate_(
				sclnjs::sCaller &Caller,
				bso::sBool RPN )
			{
			qRH
				rRackAsyncCallback_ *Rack = NULL;
			qRB
				Rack = new rRackAsyncCallback_;

				if ( Rack == NULL )
					qRGnr();

				Rack->Init( RPN );

				Rack->Callback = new sclnjs::rCallback;

				if ( Rack->Callback == NULL )
					qRGnr();

				Rack->Callback->Init();

				Caller.GetArgument( Rack->Expression, *Rack->Callback );

				sclnjs::Launch( *Rack );
			qRR
				if ( Rack != NULL )	// Deletes also 'Callback'.
					delete Rack;
			qRT
			qRE
			}
		}

		SCLNJS_F( EvaluateALG_ )
		{
			Evaluate_( Caller, false );
		}

		SCLNJS_F( EvaluateRPN_ )
		{
			Evaluate_( Caller, true );
		}
	}
}

void sclnjs::SCLNJSRegister( sclnjs::sRegistrar &Registrar )
{
	Registrar.Register( ReturnArgument_ );
	Registrar.Register( EvaluateALG_, EvaluateRPN_ );
}

const char *sclmisc::SCLMISCTargetName = NAME_LC;
const char *sclmisc::SCLMISCProductName = NAME_MC;
// const char *scln4a::SCLN4AProductVersion = VERSION;
