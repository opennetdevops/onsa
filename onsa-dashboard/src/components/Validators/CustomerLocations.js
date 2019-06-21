import * as yup from "yup";

export const validationSchema = () => {
  const min = 3;
  const max = 50;
  const addressErr =
    "The Address must be between " + min + " and " + max + " characters long.";
  const descErr =
    "The Description must be less than " + max + " characters long.";

  yup.setLocale({
    string: { trim: "Check for leading and trailling spaces." }
  });

  let schema = yup.object({
    client: yup
      .string()
      .label("Client")
      .required(),
    address: yup
      .string()
      .strict(true)
      .trim()
      .min(min, addressErr)
      .max(max, addressErr)
      .required(),
    description: yup
      .string()
      .strict(true)
      .trim()
      .max(max, descErr)
  });
  return schema;
};
