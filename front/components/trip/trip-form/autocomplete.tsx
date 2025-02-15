"use client";

import AddressAutoComplete, {
	type AddressType,
} from "@/components/ui/address-autocomplete";
import { type ChangeEventHandler, useState } from "react";

interface Props {
	value: string;
	onChange: ChangeEventHandler<HTMLInputElement>;
	onBlur: () => void;
	name: string;
	ref: React.Ref<HTMLInputElement>;
}

export const AutocompleteComponent = (props: Props) => {
	const [address, setAddress] = useState<AddressType>({
		address1: "",
		address2: "",
		formattedAddress: "",
		city: "",
		region: "",
		postalCode: "",
		country: "",
		lat: 0,
		lng: 0,
	});
	const [searchInput, setSearchInput] = useState("");
	return (
		<AddressAutoComplete
			address={address}
			setAddress={setAddress}
			searchInput={searchInput}
			setSearchInput={setSearchInput}
			dialogTitle="Enter Address"
			{...props}
		/>
	);
};
