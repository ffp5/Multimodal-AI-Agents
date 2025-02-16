"use client";

import { FormMessages } from "@/components/form-messages";
import { Button } from "@/components/ui/button";
import {
	Command,
	CommandEmpty,
	CommandGroup,
	CommandList,
} from "@/components/ui/command";
import { Input } from "@/components/ui/input";
import { useDebounce } from "@/hooks/use-debounce";
import { fetcher } from "@/utils/fetcher";
import { Delete, Loader2, Pencil } from "lucide-react";
import {
	type ChangeEventHandler,
	useCallback,
	useEffect,
	useState,
} from "react";
import { useQuery } from "@tanstack/react-query";
import AddressDialog from "./address-dialog";
import { Command as CommandPrimitive } from "cmdk";

export interface AddressType {
	address1: string;
	address2: string;
	formattedAddress: string;
	city: string;
	region: string;
	postalCode: string;
	country: string;
	lat: number;
	lng: number;
	// Optionally, the API may return a placeId.
	placeId?: string;
}

interface AddressAutoCompleteProps {
	address: AddressType;
	setAddress: (address: AddressType) => void;
	searchInput: string;
	setSearchInput: (searchInput: string) => void;
	dialogTitle: string;
	showInlineError?: boolean;
	placeholder?: string;
	value: string;
	onChange: ChangeEventHandler<HTMLInputElement>;
	onBlur: () => void;
	name: string;
	ref: React.Ref<HTMLInputElement>;
	/**
	 * When true and value is "", the component will attempt to update
	 * using current location (reverse geocoding). When false, it will
	 * clear the address.
	 */
	updateWithCurrentLocation?: boolean;
}

export default function AddressAutoComplete(props: AddressAutoCompleteProps) {
	const {
		address,
		setAddress,
		dialogTitle,
		showInlineError = true,
		searchInput,
		setSearchInput,
		placeholder,
		updateWithCurrentLocation = false,
	} = props;

	// Tracks the place id used to fetch details.
	const [selectedPlaceId, setSelectedPlaceId] = useState("");
	// Controls the open/close state of the dialog (for detailed view)
	const [isOpen, setIsOpen] = useState(false);
	// We only want to auto-fetch current location once per "new trip"
	const [hasAutoFetched, setHasAutoFetched] = useState(false);
	// Indicates if the user is actively editing the input.
	const [isManualEditing, setIsManualEditing] = useState(false);

	// Query for fetching address details using selectedPlaceId.
	const { data, isLoading } = useQuery({
		queryKey: ["place", selectedPlaceId],
		queryFn: () => fetcher(`/api/address/place?placeId=${selectedPlaceId}`),
		enabled: selectedPlaceId !== "",
		refetchOnWindowFocus: false,
	});

	const adrAddress = data?.data?.adrAddress;

	// When data is returned from fetching by placeId, update the address state.
	useEffect(() => {
		if (data?.data && data.data.address) {
			const fetchedAddress = data.data.address as AddressType;
			setAddress(fetchedAddress);
			// Notify parent of the new formatted address.
			props.onChange(fetchedAddress.formattedAddress);
			props.onBlur();
		}
	}, [data, setAddress, props]);

	// Helper: clear all address-related state.
	const clearAddress = () => {
		setSelectedPlaceId("");
		setAddress({
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
		setSearchInput("");
	};

	// Effect: handle external value changes.
	useEffect(() => {
		if (props.value === "") {
			// New trip: if auto-update is enabled, we're not editing, and we haven't auto-fetched yet.
			if (
				updateWithCurrentLocation &&
				navigator.geolocation &&
				!isManualEditing &&
				!hasAutoFetched
			) {
				setHasAutoFetched(true);
				navigator.geolocation.getCurrentPosition(
					(position) => {
						const { latitude, longitude } = position.coords;
						// Call reverse-geocoding endpoint.
						fetcher(
							`/api/address/place?lat=${latitude}&lng=${longitude}`,
						)
							.then((res) => {
								if (res?.data?.address) {
									const fetchedAddress = res.data
										.address as AddressType;
									setAddress(fetchedAddress);
									props.onChange(
										fetchedAddress.formattedAddress,
									);
									props.onBlur();
									setSearchInput(
										fetchedAddress.formattedAddress,
									);
									if (fetchedAddress.placeId) {
										setSelectedPlaceId(
											fetchedAddress.placeId,
										);
									}
								} else {
									clearAddress();
								}
							})
							.catch((error) => {
								console.error(
									"Error fetching address by location:",
									error,
								);
								clearAddress();
							});
					},
					(error) => {
						console.error("Error obtaining geolocation:", error);
						clearAddress();
					},
				);
			} else {
				// If we are editing (user typing) or auto-update disabled, just clear.
				// (But note: if user is typing, we don't want to clear their text.)
				if (!isManualEditing) {
					clearAddress();
				}
			}
		} else {
			// External value is non-empty: if it doesn't match our current address or selectedPlaceId, update.
			if (
				props.value &&
				props.value !== address.formattedAddress &&
				props.value !== selectedPlaceId
			) {
				setSelectedPlaceId(props.value);
				// Reset auto-fetch flag so that if later we get an empty value, we can try auto-fetch again.
				setHasAutoFetched(false);
			}
		}
	}, [
		props.value,
		address.formattedAddress,
		selectedPlaceId,
		updateWithCurrentLocation,
		isManualEditing,
		hasAutoFetched,
		setAddress,
		setSearchInput,
		props,
	]);

	return (
		<>
			{(selectedPlaceId !== "" || address.formattedAddress) &&
			!isManualEditing ? (
				<div className="flex items-center gap-2">
					<Input
						readOnly
						value={props.value}
						onChange={props.onChange}
						onBlur={props.onBlur}
						name="address"
					/>
					<AddressDialog
						isLoading={isLoading}
						dialogTitle={dialogTitle}
						adrAddress={adrAddress}
						address={address}
						setAddress={setAddress}
						open={isOpen}
						setOpen={setIsOpen}
					>
						<Button
							disabled={isLoading}
							size="icon"
							variant="outline"
							className="shrink-0"
						>
							<Pencil className="size-4" />
						</Button>
					</AddressDialog>
					<Button
						type="reset"
						onClick={clearAddress}
						size="icon"
						variant="outline"
						className="shrink-0"
					>
						<Delete className="size-4" />
					</Button>
				</div>
			) : (
				<AddressAutoCompleteInput
					searchInput={searchInput}
					setSearchInput={setSearchInput}
					selectedPlaceId={selectedPlaceId}
					setSelectedPlaceId={setSelectedPlaceId}
					setIsOpenDialog={setIsOpen}
					showInlineError={showInlineError}
					placeholder={placeholder}
					onStartEditing={() => setIsManualEditing(true)}
					onStopEditing={() => setIsManualEditing(false)}
				/>
			)}
		</>
	);
}

interface CommonProps {
	selectedPlaceId: string;
	setSelectedPlaceId: (placeId: string) => void;
	setIsOpenDialog: (isOpen: boolean) => void;
	showInlineError?: boolean;
	searchInput: string;
	setSearchInput: (searchInput: string) => void;
	placeholder?: string;
	onStartEditing: () => void;
	onStopEditing: () => void;
}

function AddressAutoCompleteInput(props: CommonProps) {
	const {
		setSelectedPlaceId,
		selectedPlaceId,
		setIsOpenDialog,
		showInlineError,
		searchInput,
		setSearchInput,
		placeholder,
		onStartEditing,
		onStopEditing,
	} = props;

	const [isOpen, setIsOpen] = useState(false);

	const open = useCallback(() => {
		setIsOpen(true);
		onStartEditing();
	}, [onStartEditing]);

	const close = useCallback(() => {
		setIsOpen(false);
		onStopEditing();
	}, [onStopEditing]);

	const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
		if (event.key === "Escape") {
			close();
		}
	};

	const debouncedSearchInput = useDebounce(searchInput, 500);

	const { data, isLoading } = useQuery({
		queryKey: ["autocomplete", debouncedSearchInput],
		queryFn: () =>
			fetcher(`/api/address/autocomplete?input=${debouncedSearchInput}`),
		enabled: debouncedSearchInput !== "",
	});

	const predictions = data?.data || [];

	return (
		<Command
			shouldFilter={false}
			onKeyDown={handleKeyDown}
			className="overflow-visible"
		>
			<div className="flex w-full items-center justify-between rounded-lg border bg-background ring-offset-background text-sm focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2">
				<CommandPrimitive.Input
					value={searchInput}
					onValueChange={setSearchInput}
					onBlur={close}
					onFocus={open}
					placeholder={placeholder || "Enter address"}
					className="w-full p-3 rounded-lg outline-none"
				/>
			</div>
			{searchInput !== "" &&
				!isOpen &&
				!selectedPlaceId &&
				showInlineError && (
					<FormMessages
						type="error"
						className="pt-1 text-sm"
						messages={["Select a valid address from the list"]}
					/>
				)}
			{isOpen && (
				<div className="relative animate-in fade-in-0 zoom-in-95 h-auto">
					<CommandList>
						<div className="absolute top-1.5 z-50 w-full">
							<CommandGroup className="relative h-auto z-50 min-w-[8rem] overflow-hidden rounded-md border shadow-md bg-background">
								{isLoading ? (
									<div className="h-28 flex items-center justify-center">
										<Loader2 className="size-6 animate-spin" />
									</div>
								) : (
									<>
										{predictions.map(
											(prediction: {
												placePrediction: {
													placeId: string;
													place: string;
													text: { text: string };
												};
											}) => (
												<CommandPrimitive.Item
													value={
														prediction
															.placePrediction
															.text.text
													}
													onSelect={() => {
														setSearchInput("");
														setSelectedPlaceId(
															prediction
																.placePrediction
																.place,
														);
														setIsOpenDialog(true);
													}}
													className="flex select-text flex-col cursor-pointer gap-0.5 h-max p-2 px-3 rounded-md aria-selected:bg-accent aria-selected:text-accent-foreground hover:bg-accent hover:text-accent-foreground items-start"
													key={
														prediction
															.placePrediction
															.placeId
													}
													onMouseDown={(e) =>
														e.preventDefault()
													}
												>
													{
														prediction
															.placePrediction
															.text.text
													}
												</CommandPrimitive.Item>
											),
										)}
									</>
								)}
								<CommandEmpty>
									{!isLoading && predictions.length === 0 && (
										<div className="py-4 flex items-center justify-center">
											{searchInput === ""
												? "Please enter an address"
												: "No address found"}
										</div>
									)}
								</CommandEmpty>
							</CommandGroup>
						</div>
					</CommandList>
				</div>
			)}
		</Command>
	);
}
